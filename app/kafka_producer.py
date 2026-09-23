import json
from kafka import KafkaProducer

#全局生产者实例
producer = None

def init_kafka_producer():
    global producer
    if producer in None:
        #连接到本地kafka
        producer=KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            #消息序列化：把python字典转成JSON字符串，再编码为utf-8字节流
            value_serilalizer=lambda v:json.dumps(v).encode('utf-8')
        )
    return producer

def send_task_to_kafka(task_data):
    """发送任务到kafka的data_tasks主题"""
    #p=init_kafka_producer()

    # 加上 api_version 和 request_timeout_ms 避免本地连接 Docker 假死
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        #api_version=(0, 10, 1), # 兼容性设置
        request_timeout_ms=5000 # 5秒不成功就报错，别死等
    )
     # 确保 Topic 存在（如果没创建，发送会报错）
    # 假设你的 Topic 名字叫 data_tasks
    producer.send('data_tasks', value=task_data) 
    producer.flush() # 强制立刻发送
    producer.close()

    #发送消息,key用于保证同一任务进入同一分区，value是消息内容
    #future=p.send('data_tasks',value=task_data)
    #阻塞等待发送结果(生产环境通常会设为异步回调)
    #result=future.get(timeout=10)
   # return result