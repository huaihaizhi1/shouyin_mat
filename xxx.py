from flask import Flask, sessions, request, make_response, jsonify
import os
from code1 import ResponseCode, ResponseMessage
import datetime
import time
import json
from db import my_md5,PymysqlPool







with open('C:\\Users\\huaihaizhi\\Desktop\\areas.json', 'r' ,encoding='UTF-8') as f:
    a = json.load(f)    #此时a是一个字典对象

print(a)
print(len(a))
mysql = PymysqlPool()
for i in range(0,len(a)):
    id=i+1
    name=a[i]['name']
    code=a[i]['code']
    citycode=a[i]['cityCode']
    insert_sql="insert into area(id,code,name,citycode) values({0},'{1}','{2}','{3}')".format(id,code,name,citycode)
    mysql.insert(insert_sql)
mysql.dispose()
