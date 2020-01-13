#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import re
import json

workdir = os.path.split(os.path.realpath(__file__))[0]
print(workdir)
f = open(r'C:\Users\huaihaizhi\Desktop\shouyin\areas.json', 'r', encoding='utf-8')
setting = json.load(f)
print(setting)
print(type(setting))
print(len(setting))
mysql=PymysqlPool()
