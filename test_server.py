# import pika
 
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#         'localhost'))
# channel = connection.channel()
 
# channel.queue_declare(queue='hello')
 
# channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close()

# import base64,os

# dir = r'D:\Deep Learning\testimg'
# files = os.listdir(dir)
# for each_file in files:
#         print(each_file)
#         name, type = each_file.split('.')
#         path = dir + '\\'+ each_file
#         print(path)
#         with open(path,"rb") as f:#转为二进制格式
#                 base64_data = base64.b64encode(f.read())#使用base64进行加密
#                 print(base64_data.decode())
#                 new_name = name + '.txt'
#                 file=open(new_name,'wt')#写成文本格式
#                 file.write(str(base64_data))
#                 file.close()



import os

# def find_dir(dir_name):
#     file_list = []
#     for path_name, dir, files_name in os.walk(dir_name):
#         print('path_name:',path_name, 'dir:',dir,'files_name:', files_name)
#         for file in files_name:
#             print(file)
#             file_list.append(os.path.join(path_name, file))
#     return file_list

# file_list = find_dir(r'D:\Deep Learning\yolo-server-test\device')
# print(file_list[0])

from time import localtime,time
print(localtime())