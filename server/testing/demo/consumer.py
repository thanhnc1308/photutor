from json import loads
from kafka import KafkaConsumer

print('init consumer')

consumer = KafkaConsumer(
    'test_num',
    bootstrap_servers=['localhost : 9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

print('print messages:')
for message in consumer:
    data = message.value
    print(data)

print('end')
