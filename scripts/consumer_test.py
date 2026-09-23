from kafka import KafkaConsumer
import json

#创建消费者，监听data_tasks主题
consumer=KafkaConsumer(
    'data_tasks',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  #从头开始消费
    group_id='my-test-group',  # 👈 加上这行！指定一个固定的消费者组
    enable_auto_commit=True,    # 👈 加上这行，确保消费进度被记录
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("waiting for messages...")

for message in consumer:
    print(f"Received:{message.value}")