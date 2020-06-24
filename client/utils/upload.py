# -*- encoding:utf-8 -*-

import json
import codecs
import urllib.request
import requests
import os

from folders import *

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def http_post(url, data, token):  
    postdata = data  
    post = []  
    post.append(postdata)

    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': token}
    r = requests.post(url.encode('utf-8'), data=json.dumps(post).encode('utf-8'), headers=headers)

def upload(api_url, results_directory, token):

    path_url = 'upload/'
    url = api_url + path_url

    json_file = results_directory + "/results.json"

    with open(json_file,'r') as load_f:
        load_dict = (json.load(load_f, encoding="UTF-8"))

    # extracting logs
    for file in os.scandir(LOG_PATH):

        filename = os.path.basename(file)
        name = os.path.splitext(filename)[0]

        if (name == 'runtime_log'):
            with open (file, 'r') as f:
                runtime_data = json.load(f)

                load_dict.update(runtime_data)

        else:

            with open (file, 'r') as f:
                content = f.read()

            temp = {name: content}
            load_dict.update(temp)


    with open(OUTPUT_PATH + '/results_complete.json', 'w+') as results:
        results.write(json.dumps(load_dict))
        http_post(url, load_dict, token)
