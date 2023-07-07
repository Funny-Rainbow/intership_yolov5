import os
import shutil
import datetime
import cv2
import argparse
from time import sleep, localtime, time

import my_detect, sendToSQL

source = r'H:\backup\files\jsy-camera\cameraCapture'
temp = r'D:\Deep Learning\yolov5-master\my_temp\images'

def copy_files(set_date, set_time, source, temp):
    dir_list = os.listdir(source)# 遍历设备
    # 遍历图片
    for i in dir_list:
        file_path = source + '\\' + str(i)
        file_list = os.listdir(file_path)
        for j in file_list:
            # 只复制每天09:00和14:00拍摄的图片
            time_ok = j[8:10] == '09' or j[8:10] == '14'
            if j[0:8] == set_date and time_ok:
                _, fileType = j.rsplit('.')
                name, _ = j.rsplit('.' + fileType)
                name = name.replace('.', '')
                old_name = file_path + '\\' + j
                new_name = temp + '\\' + i + '_' + name + "." + fileType #文件夹名+文件名+格式
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

def main(set_date,set_time, source, temp):
    # 只有设定的那一个小时才执行一次
    if int(localtime(time())[3]) == set_time:
        try:
            os.mkdir(temp)
        except:
            print(Exception.args)
        copy_files(set_date, set_time, source, temp) # 将今天的照片临时拷贝到同一目录下
        tempDir = os.listdir(temp)
        # 判断暂存文件夹内有无图片
        print('找到了',len(tempDir),'张照片')
        if len(tempDir):
            opt = my_detect.parse_opt() # 获取需要传入ai识别的参数
            detected_files = my_detect.main(opt) # 返回识别为疑似非农化的图片名称以及置信度
            show_images(source, detected_files) # 从备份文件中查看疑似非农化的图片
        else:
            detected_files = None
            print('未发现今日图片，停止识别')
        try:
                shutil.rmtree(temp) # 每次运行结束后，删除临时照片，每次运行会因为未知原因报错，不影响使用
        except:
                print(Exception.with_traceback, '这个报错有时出现，但是能正常执行')
        
        return detected_files
    else:
         print('不在指定工作时间')


def parse_opt():
    today = str(datetime.date.today())
    today_splited = today.split('-')# 分离年月日
    today = ''
    today = str(today_splited[0])+str(today_splited[1]+str(today_splited[2])) #获取今天的日期
    #today = '20230622' #仅限测试使用
    now = localtime(time())[3]
    parser = argparse.ArgumentParser()
    args, unknown = parser.parse_known_args()
    parser.add_argument('--set_date',  type=str, default= today, help='only for test, just leave it defult')
    parser.add_argument('--set_time',  type=int, default= now, help='choose when does the process run')
    parser.add_argument('--source', type=str, default= source, help='path of the device root(not photos root)')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--temp', type=str, default= temp, help='temprorarily create a folder to store photos')
    myopt, unknown = parser.parse_known_args()
    if unknown:
         print('Unknown in my_main.py arguments:', unknown)
    return myopt


if __name__ == '__main__':
    m = 6   #设置照片显示大小
    while True:
        myopt = parse_opt()
        print('parameters:',myopt)
        detected_files = main(**vars(myopt))
        # id,create_time, name, confidence
        if detected_files:
            sendToSQL.s2S(detected_files)
            print('识别到了：', len(detected_files),'张非农化照片')
            sleep(60*60)
        print("休眠,现在时间", localtime(time())[3],"时")
        sleep(60*10)