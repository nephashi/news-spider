import os
import time

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