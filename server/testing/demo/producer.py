from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

for n in range(3):
    data = {
        'num': n
    }
    producer.send('test_num', value=data)
    sleep(2)
