## Utility

该项目是中文新闻门户网站的新闻爬虫。主要分为两部分：url爬虫和新闻页面爬虫。

url爬虫得到链接后会推送到redis队列，之后新闻爬虫会去消费该队列。因此该项目易于进行分布式部署，只需在多台主机上部署消费者即可。

爬到的新闻会存到mongodb中。

该项目较易扩展新的url爬虫，只要在spider.url_spider中模仿已有实现编写爬虫逻辑即可

## Dependency
python3.5.2

scrapy
```
sudo apt-get install libffi-dev
sudo apt-get install libssl-dev
pip3 install scrapy
```

redis
```
pip3 install Redis
```

mongoengine
```
pip3 install mongoengine
```

## Usage
执行launcher下面的脚本即可

关于实现和扩充的细节，参考doc文档

## Issue
扩充url爬虫的数量，爬取更多门户页。

在一个脚本里多次执行scrapy启动器会出现问题，暂时通过使用系统shell启动脚本绕过这个问题。