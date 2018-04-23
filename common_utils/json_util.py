import json

def dic2json(dic):
    return json.dumps(dic, ensure_ascii=False)

def json2dic(jsonstr):
    return json.loads(jsonstr)