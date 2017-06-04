from pykafka import KafkaClient
client = KafkaClient("localhost:9092")
topic = client.topics[b"tweet"]
consumer = topic.get_simple_consumer()
consumer = topic.get_simple_consumer(consumer_timeout_ms=50000)
for msg in consumer:
    print(
        "% s[key = % s, id = % s, offset = % s]" %
        (msg.value, msg.partition_key, msg.partition_id, msg.offset))