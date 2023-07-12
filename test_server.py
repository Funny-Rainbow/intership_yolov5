#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('admin', 'jm12345678')
Parameter = pika.ConnectionParameters('127.0.0.1',5672,'/',credentials)
connection = pika.BlockingConnection(Parameter)

channel = connection.channel()
# 3. 创建队列，queue_declare可以使用任意次数，
# 如果指定的queue不存在，则会创建一个queue，如果已经存在，
# 则不会做其他动作，官方推荐，每次使用时都可以加上这句
channel.queue_declare(queue='hello')
# 4. 发布消息
channel.basic_publish(
    exchange='',  # RabbitMQ中所有的消息都要先通过交换机，空字符串表示使用默认的交换机
    routing_key='hello',  # 指定消息要发送到哪个queue
    body='Hello world!')  # 消息的内容
# 5. 关闭连接
connection.close()