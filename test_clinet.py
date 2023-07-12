#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('admin', 'jm12345678')
Parameter = pika.ConnectionParameters('127.0.0.1',5672,'/',credentials)
connection = pika.BlockingConnection(Parameter)
channel = connection.channel()

# 4. 定义消息处理程序
def callback(ch, method, properties, body):
    print('[x] Received %r' % body)

def main():
# 5. 接收来自指定queue的消息
channel.basic_consume(
    queue='hello',  # 接收指定queue的消息
    on_message_callback=callback,  # 接收到消息后的处理程序
    auto_ack=True)  # 指定为True，表示消息接收到后自动给消息发送方回复确认，已收到消息
print('[*] Waiting for message.')
# 6. 开始循环等待，一直处于等待接收消息的状态
channel.start_consuming()
