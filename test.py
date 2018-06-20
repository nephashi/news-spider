#-*- coding: utf-8 -*-
import urllib.request
import gzip
import io

url='http://temp.163.com/special/00804KVA/cm_yaowen.js?callback=data_callback'
req = urllib.request.Request(url)
data = urllib.request.urlopen(req)
encoding = data.getheader('Content-Encoding')
content = data.read().decode('gb2312')

#with open('test.html',"wb") as fb:
#    fb.write(data)

print(content)