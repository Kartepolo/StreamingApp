from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

sc = SparkContext(appName="Simple_Spark_Kafka")
sc.setLogLevel("WARN")

ssc = StreamingContext(sc, 50)

directKafkaStream = KafkaUtils.createDirectStream(ssc, ["tweet"], {"metadata.broker.list": "localhost:9092"})

offsetRanges = []

def storeOffsetRanges(rdd):
    global offsetRanges
    offsetRanges = rdd.offsetRanges()
    return rdd

def printOffsetRanges(rdd):
    for o in offsetRanges:
        print ("%s %s %s %s" % (o.topic, o.partition, o.fromOffset, o.untilOffset))

directKafkaStream\
    .transform(storeOffsetRanges) \
    .foreachRDD(printOffsetRanges)