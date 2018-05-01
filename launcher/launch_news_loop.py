import os
import time
import sys
import platform

# import模块必备
def add_proj_path_to_syspath():
    sp = get_spliter()
    proj_path = sp.join(sys.path[0].split(sp)[0:-1])
    sys.path.append(proj_path)
    print('add project path: ' + proj_path + ' to system path')

def get_spliter():
    if platform.system() == "Windows":
        return '\\'
    else:
        return '/'

add_proj_path_to_syspath()

# scrapy被设计为单独的程序，难以作为库调用
# 重复调用爬虫会出错，目前只能采取这种方式了
python_command = 'C:\Python35\python.exe'
script_name = 'D:/Projects/news-spider/launcher/launch_news_ppl.py'

while (True):
    process = os.popen(python_command + ' ' + script_name)
    output = process.read()
    process.close()
    print(output)

    time.sleep(600)