import pymysql
import cv2
import argparse

m=5

def read(db_host,db_user,db_pwd,db_database):
    db = pymysql.connect(host=db_host, user= db_user, password=db_pwd, database=db_database)
# 使用cursor()创建一个cursor对象
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cvdata;')
    dbdata = cursor.fetchall()
    print(dbdata)
    return dbdata

def show_images(source, dbdata):
     print("识别到",len(dbdata),"张疑似非农化照片")
     for i in range(len(dbdata)):
          print(dbdata[i][2])
          url = source + "\\" + str(dbdata[i][2]) + "\\" + str(dbdata[i][3])
          img = cv2.imread(url)
          img = cv2.resize(img, (192*m,108*m))
          cv2.imshow("img", img)
          if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print('quit')
            break
          else:
              pass
          cv2.destroyAllWindows()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_host',  type=str, default= '127.0.0.1', help='database host')
    parser.add_argument('--db_user', type=str, default= 'root', help='database user')
    #parser.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--db_pwd', type=str, default= '##JmMyC2810', help='database password')
    parser.add_argument('--db_database', type=str, default= 'cvtest', help='database name')
    parser2 = argparse.ArgumentParser()
    parser2.add_argument('--source', type=str, default= r'H:\backup\files\jsy-camera\cameraCapture', help='device root path')
    opt2,un = parser2.parse_known_args()
    source = opt2.source
    print(source)
    dbopt, unknown = parser.parse_known_args()
    if unknown:
         print('Unknown in sql2img.py arguments:', unknown)
    return dbopt,source

if __name__ == '__main__':
    rdopt,source = parse_opt()
    dbdata = read(**vars(rdopt))
    show_images(source, dbdata)
