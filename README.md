# My_yolo

#### 介绍
{非农化识别}

#### 软件架构
完全基于Python，拥要有三个主要功能
1.照片循环识别
2.照片全部识别
3.显示数据库中的照片


#### 安装教程

1.  安装Python 3.9 环境
2.  安装Python依赖 pip install -r requirements.txt
3.  建立数据库：id(int), create_time(datetime), device(varchar(50)), file_name(varhar(50)), confidence(float)

#### 使用说明

1.  修改和运行目录下的中文脚本文件即可
2.  照片循环识别：指定set_time后，每日只会在设定的那一小时执行一次
3.  照片全部识别：一次性识别所有设备下的所有照片，可以指定每个设备识别的最大值

#### 具体参数说明
    1.数据库和检测
    共用参数：
    --db_host	        指定 数据库IP				格式：略		        默认：127.0.0.1
    --db_user	        指定 数据库用户名			格式：略		        默认：root
    --db_pwd	        指定 数据库密码				格式：略		        默认：'##JmMyC2810'
    --db_database       指定 数据库名称				格式：略		        默认：'cvtest'
    --weights	        指定 权重文件				格式：略		        默认：'best.pt'
    --data		指定 yaml文件位置			格式：略		        默认：'data/uc.yaml'
    --conf-thres	指定 识别为目标的置信度阈值		格式：Float	        默认：0.5
    
    
    2.detect_cycle.py 每日执行一次
    参数:
    --set_date	        指定 需要识别的照片是哪一天捕获的	        格式：20230624          默认：<每一次循环 执行时对应的日期>
    --set_time	        指定 每日识别的时间			格式：6		        默认：<每一小时>
    --source	        指定 监控设备根目录			格式：略		        默认：'H:\backup\files\jsy-camera\cameraCapture'
    --temp	        指定 图像暂存目录（会自动创建空目录）	格式：略		        默认：'D:\Deep Learning\yolov5-master\my_temp\images'
    
    
    3.detect_all.py 识别所有照片，运行后可以指定索引区间
    参数:
    --source	        指定 设备根目录
    --temp		指定 暂存目录
    --detect_show	指定 识别结束后是否显示图片		格式：略		        默认：False（要显示图片，在命令中添加 --detect_show 即可）
    --maxpic	        指定 每台设备识别的最大照片数		格式：Int		默认：10
    
    
    4.readFromSQL.py 根据SQL和本地文件显示识别到的疑似非农化
    参数：
    --source	        指定 设备根目录				格式：略		        默认：'H:\backup\files\jsy-camera\cameraCapture'

