#消费者
from kafka import KafkaConsumer
import time

topic = 'test'
consumer = KafkaConsumer(topic, bootstrap_servers=['jing.tk:9092'], group_id="test", auto_offset_reset="earliest")
# 参数bootstrap_servers：指定kafka连接地址
# 参数group_id：如果2个程序的topic和group_id相同，那么他们读取的数据不会重复，2个程序的topic相同，group_id不同，那么他们各自消费相同的数据，互不影响
# 参数auto_offset_reset：默认为latest表示offset设置为当前程序启动时的数据位置，earliest表示offset设置为0，在你的group_id第一次运行时，还没有offset的时候，给你设定初始offset。一旦group_id有了offset，那么此参数就不起作用了


for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    print(recv)
    # time.sleep(1)