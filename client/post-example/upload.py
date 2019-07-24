# -*- encoding:utf-8 -*-

import json
import codecs
import urllib.request
import requests


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


token = '0232f37f8e1726684516434441af745'
# BASE_URL = 'http://140.211.168.111:8080/'
BASE_URL = 'http://127.0.0.1:8000/'
PATH_URL = 'upload/'
url = BASE_URL + PATH_URL


def http_post(url, data, token):  
    postdata = data  
    post = []  
    post.append(postdata)

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.post(url.encode('utf-8'), data=json.dumps(post).encode('utf-8'), headers=headers)

    #req = urllib.request.Request(url, json.dumps(post))

    '''
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data=data)

    access_token = token  
    req.add_header('Authorization', access_token) # add token in header
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req)  
    result = json.loads(response.read())  
    print(result.encode('utf-8'))
    '''


with open("./results.json",'r') as load_f:
    load_dict = (json.load(load_f, encoding="UTF-8"))
    http_post(url, load_dict, token)
