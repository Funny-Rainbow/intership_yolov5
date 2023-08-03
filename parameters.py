import argparse
import logging
import os
from time import localtime, time
from pathlib import Path


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

"""
如果需要修改参数：
default为一般参数，的直接修改default值即可
default为store_true的意为默认为false,当传入对应参数如: --nosave 时，传入值变为true。反之为store_false时默认为true，传入 --nosave 后为false
可通过命令传参,如：python detect_mq.py --db_pwd '12345'
"""

# 创建sendToSQL.py参数😘
def s2S_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_host',  type=str, default= '47.109.32.231',               help='数据库 IP')
    parser.add_argument('--db_port', type=str, default= '5432',                         help='数据库 端口')
    parser.add_argument('--db_user', type=str, default= 'postgres',                     help='数据库 用户名')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--db_pwd', type=str, default= 'rdhy@9999',                     help='数据库 密码')
    parser.add_argument('--db_database', type=str, default= 'ai-test',                  help='数据库 名称')
    dbopt, unknown = parser.parse_known_args()
    if unknown:
         logging.debug('Unknown in sendToSQL.py arguments:', unknown)
    return dbopt

# 创建detect_mq.py参数😂
def mq_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mq_temp', type=str, default= ROOT / r"my_temp/mq_images",    help='消息队列 图片暂存位置')
    parser.add_argument('--mq_user', type=str, default= 'admin',                        help='消息队列 用户名')
    parser.add_argument('--mq_pwd', type=str, default='admin',                          help='消息队列 密码')
    parser.add_argument('--mq_ip', type=str, default='192.168.124.18',                  help='消息队列 生产者IP')
    parser.add_argument('--mq_port', type=int, default=5672,                            help='消息队列 端口')
    parser.add_argument('--mq_queue', type=str, default='building_house_ai_queue',      help='消息队列 队列名称')
    mq_opt, unknown = parser.parse_known_args()
    if unknown:
        log_temp = 'mq_Unknown in detected_mq.py arguments:', unknown
        logging.debug(log_temp)
    return mq_opt

# 创建my_detect.py参数😍
def det_opt():
    now = ''
    for i in range(6):
        temp_time = str(localtime(time())[i])
        if i >0:
            now = now + '-' + temp_time
        else:
            now = now + temp_time

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / r"best_v1.pt", help='权重文件url路径')
    parser.add_argument('--temp', type=str, default= ROOT / r'my_temp/cycle_images',    help='循环识别暂存位置（弃用）')
    #parser.add_argument('--temp', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default='data/uc.yaml',                     help='yaml url(一般情况无需修改)')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.5,                        help='识别置信度阈值')
    parser.add_argument('--iou-thres', type=float, default=0.45,                        help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000,                            help='单张图片最大识别数量')
    parser.add_argument('--device', default='',                                         help='选择cpu或gpu')
    parser.add_argument('--view-img', action='store_true',                              help='是否弹出识别结果图像')
    parser.add_argument('--save-txt', action='store_true',                              help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true',                             help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true',                             help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true',                                help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,                               help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',                          help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',                               help='图像增强')
    parser.add_argument('--visualize', action='store_true',                             help='visualize features')
    parser.add_argument('--update', action='store_true',                                help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect',                      help='保存位置 project/name')
    parser.add_argument('--name', default=now,                                          help='保存的文件名')
    parser.add_argument('--exist-ok', action='store_true',                              help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int,                        help='框边宽度（像素）')
    parser.add_argument('--hide-labels', default=False, action='store_true',            help='隐藏标签')
    parser.add_argument('--hide-conf', default=False, action='store_true',              help='隐藏置信度')
    parser.add_argument('--half', action='store_true',                                  help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true',                                   help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1,                            help='video frame-rate stride')
    
    opt, unknown = parser.parse_known_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    if unknown:
        log_temp = 'Unknown in my_detect.py arguments:', unknown
        logging.debug(log_temp)
    return opt