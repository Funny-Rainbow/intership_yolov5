import os
import shutil
import datetime
import cv2
import argparse
import random
from time import sleep, localtime, time

import my_detect, sendToSQL
"""
参数
set_time 选择一天中的一个时间来运行文件
source  照片源（应该为所有设备所在的路径）
temp    创建一个暂时存储识别照片的文件夹，识别结束后会删除
"""

source = r'H:\backup\files\jsy-camera\cameraCapture'
temp = r'D:\Deep Learning\yolov5-master\my_temp\images'

def copy_files(source, temp, maxpic, dir_list):
        
        file_path = source + '\\' + str(dir_list)
        file_list = os.listdir(file_path)
        # 控制每个设备所识别的最大图片数量
        if len(file_list) > maxpic:
            s_list = random.sample(file_list,maxpic)
        else:
            s_list = file_list
        for j in s_list:
            hello, fileType = j.rsplit('.')
            name, suffix = j.rsplit('.' + fileType)
            name = name.replace('.', '')
            old_name = file_path + '\\' + j
            new_name = temp + '\\' + dir_list + '_' + name + "." + fileType #文件夹名+文件名+格式
            shutil.copyfile(old_name, new_name)

#显示识别到的疑似非农化照片
def show_images(source, detected_files):
     print("识别到",len(detected_files),"张疑似非农化照片")
     for i in range(len(detected_files)):
          id, filename = detected_files[i][0].split("_")
          url = source + "\\" + str(id) + "\\" + str(filename)
          img = cv2.imread(url)
          img = cv2.resize(img, (192*m,108*m))
          cv2.imshow("img", img)
          cv2.waitKey(0)
          cv2.destroyAllWindows()

def main(source, temp, detect_show, maxpic):
    dir_lists = os.listdir(source)
    detected_files = []
    for dir_list in dir_lists:
        try:
            os.mkdir(temp)
        except:
            print(Exception.args)
        copy_files( source, temp, maxpic, dir_list) # 将今天的照片临时拷贝到同一目录下
        tempDir = os.listdir(temp)
        # 判断暂存文件夹内有无图片
        print('找到了',len(tempDir),'张照片')
        if len(tempDir):
            opt = my_detect.parse_opt() # 获取需要传入ai识别的参数
            detected_file = my_detect.main(opt) # 返回识别为疑似非农化的图片名称以及置信度
            detected_files = detected_files + detected_file
            if detect_show:
                show_images(source, detected_file) # 从备份文件中查看疑似非农化的图片
            else:
                    print('由参数控制，不展示识别到的图片')
        else:
            detected_file = None
            print('未发现今日图片，停止识别')
        try:
                shutil.rmtree(temp) # 每次运行结束后，删除临时照片，每次运行会因为未知原因报错，不影响使用
        except:
                print(Exception.with_traceback, '这个报错有时出现，但是能正常执行')
        print(detected_files)
    
    return detected_files


def parse_opt():
    today = str(datetime.date.today())
    today_splited = today.split('-')# 分离年月日
    today = ''
    today = str(today_splited[0])+str(today_splited[1]+str(today_splited[2])) #获取今天的日期
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default= source, help='path of the device root(not photos root)')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--temp', type=str, default= temp, help='temprorarily create a folder to store photos')
    parser.add_argument('--detect_show', action='store_true', help='show the result or not')
    parser.add_argument('--maxpic', type=int, default= 10, help='Maximum number of pictures to detect of each device')
    myopt, unknown = parser.parse_known_args()
    if unknown:
         print('Unknown in my_main.py arguments:', unknown)
    return myopt


if __name__ == '__main__':
    m = 6   #设置照片显示大小
    myopt = parse_opt()#传参
    detected_files = main(**vars(myopt))
    # id,create_time, name, confidence
    if detected_files:
        sendToSQL.s2S(detected_files)
        print(detected_files)
    print("识别全部完成")