import os
import shutil
import base64
import logging
import pika
import json
import requests
import datetime
from PIL import Image
from io import BytesIO
from pathlib import Path
from time import sleep
import my_detect, sendToSQL, parameters

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

logging_level = logging.INFO # 可调整日志文件的存储等级 建议选择INFO/DEBUG. DEBUG 会记录大量运行信息,INFO则只会记录关键日志


# 参数初始化
def init():
     if not os.path.isdir(mq_temp):
          try:
               os.mkdir(mq_temp)
          except Exception as error:
               print(error)

# 消息队列 回调函数 执行剩余指令
def callback(ch, method, properties, body):
     print('[^]消息队列收到消息 正在处理')
     logging.info('[^]消息队列收到消息 正在处理')
     mq_data = mq_data_init(body)
     if mq_data:
          channel.close()
          detected_files, undetected_files = recog() #识别
          log_temp = 'mq_在'+ str(len(detected_files)+len(undetected_files)) + '张照片中识别到' + str(len(detected_files)) + '张疑似非农化照片'
          logging.info(log_temp)
          print(log_temp)
          sendToSQL.s2S(detected_files, undetected_files, mq_data)# 将数据发送给数据库
     else:
          logging.warning('收到空数据')
          print('收到空数据')

# 接收消息队列消息
def mq_receive(mq_queue):
     global channel
     channel = connection.channel()
     #channel.queue_declare(queue=mq_queue)# 指定queue
     channel.basic_consume(
     queue=mq_queue,  # 接收指定queue的消息
     on_message_callback=callback,  # 接收到消息后的处理程序
     auto_ack=False)  # 指定为True，表示消息接收到后自动给消息发送方回复确认，已收到消息
     print('[*] 正在等待消息队列数据')
     logging.info('[*] 正在等待消息队列数据')
     # 6. 开始循环等待，一直处于等待接收消息的状态
     channel.start_consuming()

# 处理消息队列数据
def mq_data_init(mq_json):
     print('mq_json',mq_json)
     if mq_json:
          # json转list
          mq_list = json.loads(mq_json) 
          print('mq_list',mq_list)
          log_temp = 'mq_接收到' + str(len(mq_list)) + '张图片'
          logging.info(log_temp)
          log_temp = 'mq数据:' + str(mq_list)
          logging.debug(log_temp)
          # 处理数据 并根据url保存图片
          try:
               for element in mq_list:
                    pic = requests.get(element['url'])
                    save_path = str(ROOT) + '/' + 'my_temp/mq_images/' + element['name']
                    with open(save_path,"wb") as f:
                         f.write(pic.content)
          except Exception as error:
               logging.warning('json格式错误')
               print('json格式错误')
     else:
          mq_list = None
     return mq_list

# Base64转图片(弃用)
def b64_decode(file_name, base64_string, save_path):
     decoded_image_data = base64.b64decode(base64_string)
     image = Image.open(BytesIO(decoded_image_data))
     image.save(str(save_path) + "\\" + file_name)

# 识别
def recog():
    opt = parameters.det_opt() # 获取需要传入ai识别的参数
    #opt.temp = mq_temp
    opt.temp = mq_temp
    detected_files, undetected_files = my_detect.main(opt) # 检测到的图片和未检测到的分开返回，返回名称，识别框和置信度
    return detected_files, undetected_files

# 删除临时照片
def delete_temp():
     if os.path.isdir(mq_temp):
          try:
               shutil.rmtree(mq_temp) # 每次运行结束后，删除临时照片
          except Exception as error:
               print(error, '文件夹已被删除')


# 主函数，循环监听
def main():
     global connection
     global mq_temp
     mq_opt = parameters.mq_opt()# 获取参数
     mq_temp = mq_opt.mq_temp # 传入消息队列图片临时存放路径
     mq_user = mq_opt.mq_user
     mq_pwd  = mq_opt.mq_pwd
     mq_ip  = mq_opt.mq_ip
     mq_port  = mq_opt.mq_port
     mq_queue = mq_opt.mq_queue

     # 创建消息队列连接
     credentials = pika.PlainCredentials(mq_user, mq_pwd)
     Parameter = pika.ConnectionParameters(mq_ip,mq_port,'/',credentials)
     connection = pika.BlockingConnection(Parameter)

     # 创建日志
     logging.info('mq_启动')
     print('mq_启动')
     while True:
          delete_temp()  #删除临时文件夹和未删掉的照片
          init()         #重新创建临时文件夹
          mq_receive(mq_queue)   #等待消息队列消息
          delete_temp()  #删除临时文件夹和照片
          
          logging.info("mq_本次结束")
          print('mq_本次结束')
          sleep(0.5)       #多线程需要sleep

if __name__ == '__main__':
     today = str(datetime.date.today())

     # 创建用于存放日志和临时图片的文件夹
     if not os.path.isdir(ROOT / 'log'):
          try:
               os.mkdir(ROOT / 'log')
          except Exception as error:
               print(error)
     
     if not os.path.isdir(ROOT / 'my_temp'):
          try:
               os.mkdir(ROOT / 'my_temp')
          except Exception as error:
               print(error)

     # 配置 log 文件
     log_name = 'log/mq_' + today + '.log'
     log_name = ROOT / log_name
     logging.basicConfig(filename= log_name, #文件名
                         level=logging_level, #存储等级（文件最上方修改）
                         format='%(asctime)s-%(name)s-%(levelname)s - %(message)s', # 日志的格式
                         datefmt='%m/%d %H:%M:%S',) # 时间的格式 月/日 时:分:秒
     main()