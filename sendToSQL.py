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
        for k in all_data: # 匹配并合并数据，将
            for l in mq_data:
                if k[1] == l[0]:
                    k = k + l[1:]
                    data.append(k)
    else:
        print('数据长度错误')
        logging.warning('数据长度错误')
    return data


def send(db, cursor, data):
    try:
    # 执行SQL,插入多条数据
        cursor.executemany("insert into cv_table(create_time, file_name, det_data, non_argric, url, source_id, source_type, geo) values (%s,%s,%s,%s,%s,%s,%s,%s)", data)# id由数据库自动填充

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