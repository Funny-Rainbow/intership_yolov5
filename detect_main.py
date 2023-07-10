import detect_cycle,detect_mq,logging
from threading import Thread, current_thread
"""
多级目录？
rabbitMQ 格式是怎样的？
日志全部输出？
微
"""

def main():
    logging.basicConfig(filename= r'D:\Deep Learning\yolov5-server_v2\log\example.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

    # 创建线程
    thread01 = Thread(target=detect_cycle.main, name="线程1")
    thread02 = Thread(target=detect_mq.main, name="线程2")
    # 启动线程
    thread01.start()
    thread02.start()


if __name__ == "__main__":
    main()