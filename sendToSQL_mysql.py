import pymysql
import logging
import datetime
import argparse
import json
# 数据库格式：
#     1          2                  3             4                  5
# id(int), create_time(datetime), device(str), file_name(str), confidence(float)

# 连接数据库
def init(db_host,db_user,db_pwd,db_database):
    db = pymysql.connect(host=db_host, user= db_user, password=db_pwd, database=db_database)
    # 使用cursor()创建一个cursor对象
    cursor = db.cursor()
    return db, cursor

# 数据格式初始化
def dataInit(detected_files, undetected_files,l data):
    de_data = []
    un_data = []
    now = datetime.datetime.now()
        if detected_files:
            for i in detected_files:
                de_file_name = i[0]
                file_data = json.dumps(i[1])
                new_data = [now, de_file_name, file_data, 1]
                de_data.append(new_data)
        if undetected_files:
            for j in undetected_files:
                un_file_name = j
                new_un_data = [now, un_file_name, None, 0]
                un_data.append(new_un_data)
    return de_data + un_data

def send(db, cursor, data):
    try:
    # 执行SQL,插入多条数据
        cursor.executemany("insert into cv_data(create_time, file_name, detect_data, non_argric) values (%s,%s,%s,%s)", data)# id由数据库自动填充

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
def s2S(detected_files, undetected_files):
    #获取参数
    dbopt = parse_opt()
    #数据库初始化
    db,cursor = init(**vars(dbopt))
    #数据处理
    data = dataInit(detected_files, undetected_files)
    #发送到数据库
    send(db, cursor, data)

# 创建参数
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_host',  type=str, default= '127.0.0.1', help='database host')
    parser.add_argument('--db_user', type=str, default= 'root', help='database user')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--db_pwd', type=str, default= '##JmMyC2810', help='database password')
    parser.add_argument('--db_database', type=str, default= 'cv_db', help='database name')
    dbopt, unknown = parser.parse_known_args()
    if unknown:
         logging.debug('Unknown in sendToSQL.py arguments:', unknown)
    return dbopt

if __name__ == '__main__':
    old_data = [['20210903130602.jpg', [[62.769989013671875, 10.444976806640625, 634.982177734375, 422.5649108886719, 0.8292975425720215]],1]]
    s2S(old_data,None)