# 生产者
from kafka import KafkaProducer
import json
import datetime

topic = 'test'
producer = KafkaProducer(bootstrap_servers='jing.tk:50045',
                         value_serializer=lambda m: json.dumps(m).encode("utf-8"))  # 连接kafka
# 参数bootstrap_servers：指定kafka连接地址
# 参数value_serializer：指定序列化的方式，我们定义json来序列化数据，当字典传入kafka时自动转换成bytes
# 用户密码登入参数
# security_protocol="SASL_PLAINTEXT"
# sasl_mechanism="PLAIN"
# sasl_plain_username="maple"
# sasl_plain_password="maple"

for i in range(1000):
    data = {"num": i, "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    producer.send(topic, data)

producer.close()
