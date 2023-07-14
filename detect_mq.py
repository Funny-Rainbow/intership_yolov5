import os
import shutil
import argparse
import base64
import logging
import pika
import json
from PIL import Image
from io import BytesIO
from pathlib import Path
from time import sleep
import my_detect, sendToSQL

credentials = pika.PlainCredentials('admin', 'jm12345678')
Parameter = pika.ConnectionParameters('127.0.0.1',5672,'/',credentials)
connection = pika.BlockingConnection(Parameter)
global channel

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

# 参数初始化
def init():
     if not os.path.isdir(mq_temp):
          try:
               os.mkdir(mq_temp)
          except Exception as error:
               print(error)

def callback(ch, method, properties, body):
    print('[^]消息队列收到消息')
    logging.info('[^]消息队列收到消息')
    mq_data_init(body)
    channel.close()

# 接收消息队列消息
def mq_receive():
     global channel
     channel = connection.channel()
     channel.queue_declare(queue='cv')
     channel.basic_consume(
     queue='cv',  # 接收指定queue的消息
     on_message_callback=callback,  # 接收到消息后的处理程序
     auto_ack=True)  # 指定为True，表示消息接收到后自动给消息发送方回复确认，已收到消息
     print('[*] 正在等待消息队列数据')
     logging.info('[*] 正在等待消息队列数据')
     # 6. 开始循环等待，一直处于等待接收消息的状态
     channel.start_consuming()

# 处理消息队列数据
def mq_data_init(mq_json):
     mq_list = json.loads(mq_json)
     log_temp = 'mq_接收到' + str(len(mq_json)) + '张图片'
     logging.info(log_temp)
     for element in mq_list:
         file_name = element['name']
         base64_string = element['base64']
         b64_decode(file_name, base64_string, mq_temp)

# Base64转图片
def b64_decode(file_name, base64_string, save_path):
     decoded_image_data = base64.b64decode(base64_string)
     image = Image.open(BytesIO(decoded_image_data))
     image.save(str(save_path) + "\\" + file_name)

# 识别
def recog():
    opt = my_detect.parse_opt() # 获取需要传入ai识别的参数
    #opt.temp = mq_temp
    opt.temp = mq_temp
    detected_files, undetected_files = my_detect.main(opt) # 返回识别为疑似非农化的图片名称以及置信度
    return detected_files, undetected_files

# 删除临时照片
def delete_temp():
     if os.path.isdir(mq_temp):
          try:
               shutil.rmtree(mq_temp) # 每次运行结束后，删除临时照片，每次运行会因为未知原因报错，不影响使用
          except Exception as error:
               print(error, '文件夹已被删除')

# 创建参数
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mq_temp', type=str, default=ROOT / r"my_temp/mq_images", help='temporarily store recieved imgs')
    mq_opt, unknown = parser.parse_known_args()
    if unknown:
        log_temp = 'mq_Unknown in detected_mq.py arguments:', unknown
        logging.debug(log_temp)
    return mq_opt


# 主函数，循环监听
def main():
     while True:
          logging.info("mq_线程运行")
          print('正在运行mq线程')

          mq_opt = parse_opt()# 获取参数
          global mq_temp
          mq_temp = mq_opt.mq_temp

          delete_temp()  #删除临时文件夹和未删掉的照片
          init()         #重新创建临时文件夹
          mq_receive()   #等待消息队列消息
          detected_files, undetected_files = recog() #识别
          log_temp = 'mq_在'+ str(len(detected_files)+len(undetected_files)) + '张照片中识别到' + str(len(detected_files)) + '张疑似非农化照片'
          logging.info(log_temp)
          sendToSQL.s2S(detected_files, undetected_files)# 将数据发送给数据库
          delete_temp()  #删除临时文件夹和照片
          
          logging.info("mq_线程休眠")
          print('mq线程休眠')
          sleep(1)       #多线程需要sleep

if __name__ == '__main__':
    main()