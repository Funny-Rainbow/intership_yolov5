import psycopg2
import logging
import datetime
import json

import parameters
# postgresql

# 连接数据库
def init(db_host,db_port, db_user,db_pwd,db_database):
    try:
        db = psycopg2.connect(host=db_host, user= db_user, password=db_pwd, dbname=db_database, port=db_port)
        # 使用cursor()创建一个cursor对象
        cursor = db.cursor()
        return db, cursor
    except Exception as error:
        log_temp = '连接数据库失败，请检查数据库和网络状态,error:' + str(error)
        logging.warning(log_temp)

# 匹配 识别得到的数据 和 消息队列发来的数据
def match(all_data, mq_data):
    data = []
    for i in mq_data:
        for j in all_data:
            if j[1] == i['name']:
                data_temp = j + [i['url']] + [i['sourceId']] + [i['sourceType']] + [i['itude']] + [i['captureTime']] + [i['equipmentId']] # 此处顺序需要与后续插入数据库的命令中数据的顺序一致
                data.append(data_temp)
                break
    return data

# 数据格式初始化
def dataInit(detected_files, undetected_files, mq_data):
    de_data = []
    un_data = []
    data = []
    now = datetime.datetime.now()
    if len(detected_files)+len(undetected_files) == len(mq_data):
        if detected_files:
            for i in detected_files: # 处理检测到非农化的数据
                de_file_name = i[0]
                file_data = json.dumps(i[1])
                new_data = [now, de_file_name, file_data, '1']
                de_data.append(new_data)
        if undetected_files: # 处理未检测到非农化的数据
            for j in undetected_files:
                un_file_name = j
                new_un_data = [now, un_file_name, None, '0']
                un_data.append(new_un_data)
        all_data =  de_data + un_data #合并监测到非农化与未检测到的数据
        data = match(all_data, mq_data)

    else:
        print('数据长度错误')
        logging.warning('数据长度错误')
    print('data', data)
    return data

def send(db, cursor, data):
    if data:
        try:
        # 执行SQL,插入多条数据
            cursor.executemany("insert into ai_table(create_time, file_name, det_data, non_argric, url, source_id, source_type, geo, capture_time, equipment_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)# 此处顺序需要与上方产生数据的顺序一致

            # 提交数据
            db.commit()
            logging.info('数据已成功写入数据库')
            print('数据已成功写入数据库')
        
        except Exception as error:
            # 发生错误时回滚
            db.rollback()
            logging.error('数据库发生错误，终止导入数据:',error)
            print('数据库发生错误，终止导入数据:',error)

        # 关闭数据库连接
        db.close()
    else:
        logging.warning('未能生成数据库数据，请检查')
        print('未能生成数据库数据，请检查')

# 主函数  
def s2S(detected_files, undetected_files, mq_data):
    #获取参数
    dbopt = parameters.s2S_opt()
    #数据库初始化
    db,cursor = init(**vars(dbopt))
    #数据处理
    data = dataInit(detected_files, undetected_files, mq_data)
    #发送到数据库
    send(db, cursor, data)