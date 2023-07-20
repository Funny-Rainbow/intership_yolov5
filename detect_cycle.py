import os
import shutil
import datetime
import cv2
import argparse
import logging
import sys
from pathlib import Path
from time import sleep, localtime, time

import my_detect, sendToSQL


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

source = r'H:\backup\files\jsy-camera\cameraCapture'
cycle_temp = str(ROOT / r'my_temp/cycle_images')

m = 6   #设置照片显示大小

def copy_files(set_date, set_time, source, cycle_temp):
    dir_list = os.listdir(source)# 遍历设备
    file_list = []
    for path_name, dir, files_name in os.walk(source):
        for file in files_name:
            file_list.append(os.path.join(path_name, file))
    # 遍历图片
        for j in files_name:
            f_name,f_type = j.split('.')
            # 只复制每天09:00和14:00拍摄的图片
            time_ok = j[8:10] == '09' or j[8:10] == '14'
            # 只复制以下格式的图片
            type_ok = f_type == 'jpg' or f_type == 'jpeg' or f_type == 'png'
            if j[0:8] == set_date and time_ok and type_ok:
                _, fileType = j.rsplit('.')
                name, _ = j.rsplit('.' + fileType)
                name = name.replace('.', '')
                old_name = path_name + '\\' + j
                new_name = cycle_temp + '\\' + name + "." + fileType #文件夹名+文件名+格式
                shutil.copyfile(old_name, new_name)

#显示识别到的疑似非农化照片(默认关闭此功能)
def show_images(source, detected_files):
     log_temp = "cycle_识别到" + str(len(detected_files)) + "张疑似非农化照片"
     logging.info(log_temp)
     for i in range(len(detected_files)):
          id, filename = detected_files[i][0].split("_")
          url = source + "\\" + str(id) + "\\" + str(filename)
          img = cv2.imread(url)
          img = cv2.resize(img, (192*m,108*m))
          cv2.imshow("img", img)
          cv2.waitKey(0)
          cv2.destroyAllWindows()

def recog(set_date,set_time, source, cycle_temp):

    # 只有在规定时间才执行
    if int(localtime(time())[3]) == set_time:
        if os.path.isdir(cycle_temp):
            try:
                shutil.rmtree(cycle_temp) # 每次运行结束后，删除临时照片，每次运行会因为未知原因报错，不影响使用
            except Exception as error:
                print(error, '文件夹已被删除')
        if not os.path.isdir(cycle_temp):
            try:
                os.mkdir(cycle_temp)
            except Exception as error:
                print(error)
        
        copy_files(set_date, set_time, source, cycle_temp) # 将不同设备下的照片临时拷贝到同一目录下，便于后续识别
        tempDir = os.listdir(cycle_temp)
        # 判断暂存文件夹内有无图片
        log_temp = 'cycle_找到了' + str(len(tempDir)) + '张照片'
        logging.info(log_temp)
        if len(tempDir):
            opt = my_detect.parse_opt() # 获取需要传入ai识别的参数
            opt.temp = cycle_temp # 传入cycle的缓存路径
            detected_files, undetected_files = my_detect.main(opt) # 返回识别为疑似非农化的图片名称以及置信度
            #show_images(source, detected_files) # 从备份文件中查看疑似非农化的图片
        else:
            detected_files = None
            undetected_files = None
            
            logging.info('cycle_未发现今日图片，停止识别')
        try:
                shutil.rmtree(cycle_temp) # 每次运行结束后，删除临时照片，每次运行会因为未知原因报错，不影响使用
        except Exception as error:
                print(error, '文件夹已被删除')
        
        return detected_files,undetected_files
    else:
         logging.info('cycle_不在指定工作时间')
         return None,None

# 获取参数
def parse_opt():
    yesterday = str(datetime.date.today() + datetime.timedelta(-1))
    yesterday_splited = yesterday.split('-')# 分离年月日
    yesterday = ''
    yesterday = str(yesterday_splited[0])+str(yesterday_splited[1]+str(yesterday_splited[2])) #获取今天的日期
    yesterday = '20230622' #仅限测试使用
    #now = localtime(time())[3]
    parser = argparse.ArgumentParser()
    args, unknown = parser.parse_known_args()
    parser.add_argument('--set_date',  type=str, default= yesterday, help='only for test, just leave it defult')
    parser.add_argument('--set_time',  type=int, default= 23, help='choose when does the process run')
    parser.add_argument('--source', type=str, default= source, help='path of the device root(not photos root)')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--cycle_temp', type=str, default= cycle_temp, help='temprorarily create a folder to store photos')
    myopt, unknown = parser.parse_known_args()
    if unknown:
         print('Unknown in detect_cycle.py arguments:', unknown)
    return myopt


# 主函数
def main():
    while True:
        logging.info("cycle_线程运行")
        print('正在运行cycle线程')

        # 获取参数
        myopt = parse_opt()
        log_temp = 'cycle_parameters:' + str(myopt)
        logging.debug(log_temp)

        #识别
        detected_files, undetected_files = recog(**vars(myopt))
        # id,create_time, name, confidence
        if detected_files or undetected_files:
            log_temp = 'cycle_undetected_files:' + str(undetected_files)
            logging.info(log_temp)
            log_temp = 'detected_files:' + str(detected_files)
            logging.info(log_temp)
            sendToSQL.s2S(detected_files, undetected_files)
            toatal = len(undetected_files)+len(detected_files)
            log_temp = 'cycle_在' + str(toatal) + '张照片中识别到了：' + str(len(detected_files)) + '张疑似非农化照片'
            logging.info(log_temp)
            print('cycle_在', len(undetected_files), '张照片中识别到了：', len(detected_files),'张非农化照片')
        else:
             print('未找到照片')
             logging.info('cycle_未找到照片')

        # 完成/未到规定时间就休眠
        log_temp = 'cycle_休眠,现在时间' + str(localtime(time())[3]) + '时'
        logging.info(log_temp)
        print("休眠,现在时间", localtime(time())[3],"时")
        logging.info("cycle_线程休眠")
        print('cycle线程休眠')
        sleep(60)# 多线程，不可删sleep

if __name__ == '__main__':
     log_name = ROOT / 'log/cycle_test.log'
     logging.basicConfig(filename= log_name, 
                        level=logging.DEBUG, 
                        format='%(asctime)s-%(name)s-%(levelname)s - %(message)s',
                        datefmt='%m/%d %H:%M:%S',)
     main()