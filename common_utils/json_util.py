import json

def py2json(dic):
    return json.dumps(dic, ensure_ascii=False)

def json2py(jsonstr):
    return json.loads(jsonstr)