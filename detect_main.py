import detect_cycle,detect_mq,logging
from threading import Thread
import datetime

"""
多级目录?ok
rabbitMQ 格式是怎样的？
日志全部输出ok
每次输出到不同的日志ok
数据库中如何存储已经完成了识别的文件ok
"""

now = str(datetime.date.today())
log_name = 'D:\Deep Learning\\yolov5-server_v2\\log\\' +now + '.'+'log'
def main():
    logging.basicConfig(filename= log_name, 
                        level=logging.DEBUG, 
                        format='%(asctime)s-%(name)s-%(levelname)s-%(funcName)s-%(message)s',
                        datefmt='%m/%d %H:%M:%S',)

    # 创建线程
    thread01 = Thread(target=detect_cycle.main, name="线程1")
    thread02 = Thread(target=detect_mq.main, name="线程2")

    # 启动线程
    thread01.start()
    thread02.start()


if __name__ == "__main__":
    main()