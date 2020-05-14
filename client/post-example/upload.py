# -*- encoding:utf-8 -*-

import json
import codecs
import urllib.request
import requests


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


token = 'bae596fd98f42bfde08b41bfd8401b49'
BASE_URL = 'http://140.211.168.111:8080/'
PATH_URL = 'upload/'
url = BASE_URL + PATH_URL


def http_post(url, data, token):  
    postdata = data  
    post = []  
    post.append(postdata)

    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': token}
    r = requests.post(url.encode('utf-8'), data=json.dumps(post).encode('utf-8'), headers=headers)


with open("./results-linux.json",'r') as load_f:
    load_dict = (json.load(load_f, encoding="UTF-8"))
    http_post(url, load_dict, token)
