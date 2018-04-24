import re

exclude = [
    'yunqi.qq.com',
    'v.qq.com',
    'class.qq.com',
    'chuangshi.qq.com'
]

## rule: at least 6 Chinese characters or English character)
def checkTitle(title):
    return title != None and re.search(u'[\u4e00-\u9fa5]{6,}?|([a-z]|[A-Z]){6,}?', title)

## rule: 1、http or https protocol; 2、exclude some special domain names from the exclude-list
def checkLink(link):
    test = r'^https?://(?!%s)(/?)' % '|'.join(exclude)
    print(test)
    return link != None and re.search(test,link)