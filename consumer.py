from kafka import KafkaConsumer
from json import loads
import json

KAFKA_TOPIC_NAME_CONS="p3_topic"

consumer = KafkaConsumer(
    "p3_topic",
    bootstrap_servers['localhost:9092'],
    auto_offset_rest=beginning,
    enable_auto_commit=True,
    
        
        )

for message in consumer:
    print(message )