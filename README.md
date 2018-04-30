## Utility
完成了新浪主页的简单爬取, 拿到页面后会分析包含的链接，爬到的url会被送入redis. 分析完主页之后进入休眠，之后继续分析。
内部实现了一个以时间分级的多级哈希表缓存记录爬过的url以去重。缓存填满后，较早进入的项会被删除。

完成了新闻页爬取，这里会从redis读url，进一步去爬页面，爬到的新闻会做简单筛选，送入mongodb。
队列读空后进入休眠，之后继续读队列并进行爬取。

完成了mongodb持久化模块.

## Dependency
python3.5.2

scrapy

redis

mongoengine

## Usage
执行launcher下面的脚本即可

## Issue
在一个脚本里多次执行scrapy启动器会出现问题，暂时通过使用系统shell启动脚本绕过这个问题。