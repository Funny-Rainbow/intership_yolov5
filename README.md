# My_yolo

#### 介绍
{非农化识别}

#### 软件架构
完全基于Python，拥要有三个主要功能
1.照片循环识别
2.消息队列照片识别
3.上述两个功能双线程实现


#### 安装教程

1.  安装Python 3.9 环境
2.  安装Python依赖 pip install -r requirements.txt
3.  根据环境安装CUDA
4.  (可选)安装Pytorch、torchvision的GPU版本(默认为CPU版本)
3.  建立postgre sql：id(bigint), create_time(timestamp), file_name(bpchar), detect_data(json), non_argric(boolean)

#### 使用说明

1.  确认环境安装完成后，运行对应文件
2.  照片循环识别：指定set_time后，每日只会在设定的那一小时执行一次
3.  照片消息队列识别：接收到消息队列后，将base64转化为图片，并进行识别

#### 具体参数说明
    1.数据库和检测
    共用参数：
    --db_host	        指定 数据库IP				格式：略		        默认：127.0.0.1
    --db_port           指定 数据库端口             格式：int               默认:5432
    --db_user	        指定 数据库用户名			格式：略		        默认：postgres
    --db_pwd	        指定 数据库密码				格式：略		        默认：'jm12345678'
    --db_database       指定 数据库名称				格式：略		        默认：'cv_db'
    --weights	        指定 权重文件				格式：略		        默认：'best_v1.pt'（不需要换检测模型就保持不动）
    --data		指定 yaml文件位置			格式：略		        默认：'data/uc.yaml'（不需要换检测模型就保持不动）
    --conf-thres	指定 识别为目标的置信度阈值		格式：Float	        	默认：0.5
    
    
    2.detect_cycle.py 每日执行一次
    参数:
    --set_date	        指定 需要识别的照片是哪一天捕获的	格式：20230624          	默认：<昨天>
    --set_time	        指定 每日识别的时间			格式：6		        	默认：11
    --source	        指定 监控设备根目录			格式：略		        默认：'H:\backup\files\jsy-camera\cameraCapture'
    --cycle_temp	指定 循环识别图像暂存目录		格式：略		        默认：ROOT / 'my_temp/cycle_images'
    
    
    3.detect_mq.py 处理消息队列
    参数:
    --mq_temp	指定 消息队列图像暂存目录		格式：略		        默认：ROOT / 'my_temp/mq_images'	
    --mq_user		指定 消息队列用户名			格式：str			默认：'admin'
    --mq_pwd		指定 消息队密码				格式：str			默认：'jm12345678'
    --mq_ip		指定 消息队列ip				格式：str			默认：'127.0.0.1'
    --mq_port		指定 消息队列端口			格式：int			默认：5672

    4.detect_main.py 同时运行上述两个程序，可传入上述所有参数