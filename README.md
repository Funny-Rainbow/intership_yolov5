# My_yolo

#### 介绍
{非农化识别}

#### 软件架构
基于
Python语言
PostgreSQL
Rabbit MQ

#### 安装教程

1.  安装Python 3.9 环境
2.  安装Python依赖 pip install -r requirements.txt
3.  (可选,使用gpu)根据显卡安装CUDA，并安装对应的Pytorch、torchvision的GPU版本
4.  建立postgre sql：id(bigint), create_time(timestamp), file_name(bpchar), detect_data(json), non_argric(boolean)

#### 使用GPU说明
默认使用CPU，识别一张图片耗时约500ms；使用GPU耗时约40ms
GPU环境配置：
1. 前往Nvidia官网查找显卡所适配的cuda版本
2. 安装cuda
3. 前往Pytorch官网查找cuda所对应的torch版本
4. 根据Pytorch官网指引安装torch和torchvision的对应GPU版本

#### 使用说明

1.  确认环境安装完成后，运行对应文件
2.  照片消息队列识别：接收到消息队列后，根据url下载图片，并进行识别
3.  识别完成后会将识别到的图像结果保存到runs/detect中，其他存入数据库中

#### 具体参数说明(所有参数的默认值均可在parameters.py修改)
    1.数据库和检测
    参数：
    --db_host	        指定 数据库IP				格式：略		        默认：127.0.0.1
    --db_port           指定 数据库端口             格式：int               默认:5432
    --db_user	        指定 数据库用户名			格式：略		        默认：postgres
    --db_pwd	        指定 数据库密码				格式：略		        默认：'jm12345678'
    --db_database       指定 数据库名称				格式：略		        默认：'cv_db'
    --weights	        指定 权重文件				格式：略		        默认：'best_v1.pt'（不需要换检测模型就保持不动）
    --data		指定 yaml文件位置			格式：略		        默认：'data/uc.yaml'（不需要换检测模型就保持不动）
    --conf-thres	指定 识别为目标的置信度阈值		格式：Float	        	默认：0.5
    
    
    2.detect_mq.py 处理消息队列
    参数:
    --mq_temp	指定 消息队列图像暂存目录		格式：略		        默认：ROOT / 'my_temp/mq_images'	
    --mq_user		指定 消息队列用户名			格式：str			默认：'admin'
    --mq_pwd		指定 消息队密码				格式：str			默认：'jm12345678'
    --mq_ip		指定 消息队列ip				格式：str			默认：'127.0.0.1'
    --mq_port		指定 消息队列端口			格式：int			默认：5672