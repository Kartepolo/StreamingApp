import json, logging
import time

from datetime import datetime
from tweepy import StreamListener, OAuthHandler, Stream
from pykafka import KafkaClient
from model.tweet import Tweet
import tornado.gen as gen
import re


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


UTF_CHARS = r'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
TAG_EXP = r'(^|[^0-9A-Z&/]+)(#|\uff03)([0-9A-Z_]*[A-Z_]+[%s]*)' % UTF_CHARS
h = re.compile(TAG_EXP, re.UNICODE | re.IGNORECASE)
client = KafkaClient("localhost:9092")
topic = client.topics[b"tweet"]

class Listener(StreamListener):
    def __init__(self, time_limit):
        StreamListener.__init__(self)

        self.start_time = time.time()
        self.limit = time_limit

        self.kafka_producer = topic.get_producer()

        self._end_streaming = False

        self.http_error_count = 0
        self.http_420_error = 0

    def on_data(self, raw_data):
        self.http_error_count = self.http_420_error = 0
        if time.time() - self.start_time < self.limit:
            try:
                data = json.loads(raw_data)
                if not data:
                    return True
                self.add_tweet(data)
                return True
            except BaseException as e:
                logging.warning("Failed on fetching data due to", e)
                time.sleep(5)
                pass
        else:
            return False

    def on_status(self, status):
        print("on_status",status)

    def on_disconnect(self, notice):
        print("on_notice",notice)
        time.sleep(10)

    def on_error(self, status_code):
        if status_code == 420:
            self.http_420_error += 1
        else:
            self.http_error_count += 1
        self.reconnect_delay = max(min(self.http_error_count * 5, 320), self.http_420_error * 60)
        logging.warning("Error code %s . Waiting %s seconds to reconnect" % (status_code, self.reconnect_delay))
        time.sleep(self.reconnect_delay)
        self.reconnect_delay *= 2

    def add_tweet(self, data):
        try:
            raw_tweet = data['text']
            hashtags = h.match(raw_tweet)
            content = h.sub('', raw_tweet)
            timestamp = data['created_at']
            if data['coordinates'] is not None:
                coords = data['coordinates']['coordinates']
            elif data['place']:
                place = data['place']['bounding_box']['coordinates'][0]
                coords = [(place[0][0] + place[-1][0]) / 2, (place[0][1] + place[1][1]) / 2]
            else:
                return
            self.kafka_producer.produce(content.encode('utf-8'))
            return
        except Exception as e:
            logging.debug(e)

if __name__ == '__main__':

    listener = Listener(30)
    ckey = 'wWhZTi69MmcdkR0jexvPQmYjI'
    consumer_secret = 'pYbgebyMty1yf7ljLpMR8Nn6XIC5hxe5wxqTU1wbl71yjwn4gy'
    access_token_key = '830220041039785985-hdah7MHSoXMPBiTQB1VXxwacWEVQ6cO'
    access_token_secret = 'YjAtWG9QzPbsAksGEuTYYk6sNuZcZa97UvFAJGdvYXM7T'
    auth = OAuthHandler(ckey, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    st = Stream(auth, listener)
    st.filter(track=["US"])
    print ("Done")
    exit()


