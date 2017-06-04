from tornado import gen
from base import BaseHandler
from model.tweet import Tweet


import json

class TweetHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        coord = json.loads(self.get_argument("body"))
        tweets = yield self.query_db(self.db, ** coord['query'])
        if self.request.connection.stream.closed():
            return
        self.write(dict(tweets=tweets))

    @gen.coroutine
    def query_db(self, db_session, lat, lon, rng):
        yield db_session.query(Tweet).filter(Tweet.lat >= lat - rng
                                             & Tweet.lat <= lat + rng
                                             & Tweet.lon >= lon - rng
                                             & Tweet.lon <= lon + rng)