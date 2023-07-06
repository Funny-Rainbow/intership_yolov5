import pymysql
import datetime
import argparse
# 数据库格式：
#     1          2                  3             4                  5
# id(int), create_time(datetime), device(str), file_name(str), confidence(float)

# 连接数据库
def init(db_host,db_user,db_pwd,db_database):
    db = pymysql.connect(host=db_host, user= db_user, password=db_pwd, database=db_database)
    # 使用cursor()创建一个cursor对象
    cursor = db.cursor()
    return db, cursor

# 数据列表
def dataInit(old_data):
    data = []
    for i in old_data:
        confidence = i[1]
        now = datetime.datetime.now()
        device, name = i[0].split('_')
        new_data = [now, device, name, confidence]
        data.append(new_data)
    
    return data

def send(db, cursor, data):
    try:
    # 执行SQL,插入多条数据
        print(data)
        cursor.executemany("insert into cvdata(create_time, device, file_name, confidence) values (%s,%s,%s,%s)", data)# id由数据库自动填充

        # 提交数据
        db.commit()
        print('6')
    
    except Exception as error:
        # 发生错误时回滚
        db.rollback()
        print('database error occurs:',error)

    # 关闭数据库连接
    db.close()

# 主函数  
def s2S(old_data):
    #获取参数
    dbopt = parse_opt()
    #数据库初始化
    db,cursor = init(**vars(dbopt))
    #数据处理
    data = dataInit(cursor, old_data)
    #发送到数据库
    send(db, cursor, data)

# 创建参数
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_host',  type=str, default= '127.0.0.1', help='database host')
    parser.add_argument('--db_user', type=str, default= 'root', help='database user')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--db_pwd', type=str, default= '##JmMyC2810', help='database password')
    parser.add_argument('--db_database', type=str, default= 'cvtest', help='database name')
    dbopt, unknown = parser.parse_known_args()
    if unknown:
         print('Unknown in sendToSQL.py arguments:', unknown)
    return dbopt

if __name__ == '__main__':
    old_data = [
    ("2c948099823b15ea018275d2e0926f7f_20230622092256.jpg", "0.80"),
    ( "2c94809984a437180184d21c579043e8_20230622092744.jpg", "0.90"),]
    s2S(old_data)