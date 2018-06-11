"""
Author: Alex Lim

Module for API methods. 
GET: 
POST:
PUT:
DELETE:
"""
import requests
import json

""" Request: GET """
def send_get(url, headers, payload=None, js=True):
    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request = request.json()    
    return request

""" Request: POST """
def send_post(url, headers, data, js=True):
    request = requests.post(url, json.dumps(data), headers=headers)
    if js == True: 
        request = request.json()
    return request
