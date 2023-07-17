import detect_cycle,detect_mq,logging,sys,os
from threading import Thread
from pathlib import Path
import datetime

"""
多级目录?ok
rabbitMQ 格式是怎样的？
日志全部输出ok
每次输出到不同的日志ok
数据库中如何存储已经完成了识别的文件ok
"""

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

now = str(datetime.date.today())
log_name_temp = 'log/' + now + '.'+'log'
log_name = ROOT / log_name_temp
def main():
    #创建LOG文件并开始记录
    logging.basicConfig(filename= log_name, 
                        level=logging.INFO, 
                        format='%(asctime)s-%(name)s-%(levelname)s - %(message)s',
                        datefmt='%m/%d %H:%M:%S',)

    # 创建线程
    thread01 = Thread(target=detect_cycle.main, name="线程1")
    thread02 = Thread(target=detect_mq.main, name="线程2")

    # 启动线程
    thread01.start()
    thread02.start()


if __name__ == "__main__":
    main()