import requests

dict0 = [
    {
    'name':'2002.jpg',
    'url':'https://img-blog.csdn.net/20180710195812334?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTMxNzA1MQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70',
    'source_id':'0',
    'source_type':'jm123',
    'itude':'123,456'
    },
    {
    'name':'2023.jpg',
    'url':'https://img-blog.csdn.net/20180710200659285?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTMxNzA1MQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70',
    'source_id':'1',
    'source_type':'jm321',
    'itude':'456,654'
    }
]

need_data = []
for element in dict0:
    pic = requests.get(element['url'])
    save_path = 'my_temp/mq_images/' + element['name']
    with open(save_path,"wb") as f:
        f.write(pic.content)
    need_data.append(list(element.values()))
    for key in list(element.keys()):
        pass
