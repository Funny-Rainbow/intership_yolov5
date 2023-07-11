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

import json

json_str = [{
    'id':0,
    'base64':'gewigfs'
    },
    {
    'id':1,
    'base64':'ftfhbes'
    },{
    'id':2,
    'base64':'hgfcjmn'
    },{
    'id':3,
    'base64':'rgsdvhg'
    },
]

my_json = json.dumps(json_str)
print(my_json,type(my_json))
my_dict = json.loads(my_json)
print(my_dict,type(my_dict),'\\', my_dict[0], my_dict[0]['id'])

# for i in my_dict:
#     print(i['id'])
lists=[]
for i in my_dict:
    lists.append([i['id'],i['base64']])

print(lists)

import datetime
print(datetime.date.today())