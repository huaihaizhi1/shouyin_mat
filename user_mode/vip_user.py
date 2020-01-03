#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import re


def vip_user(request_body, path):
    if path=='/insert_vipuser':
        shop_id=request_body.get('id','')
        vip_id=request_body.get('vip_id','')
        vip_name=request_body.get('vip_name','')
        vip_tel_no=request_body.get('vip_tel_no','')
        sex=request_body.get('sex','')
        vip_grade=request_body.get('vip_grade','')
        if request_body.get('birthday','')=='':
            birthday=None
        else:
            birthday=date_s_date(request_body.get('birthday',''),'GMT','day')
        remark=request_body.get('remark','')
        date=get_date(0,2)
        insert_sql="insert into vip_table(shop_id,vip_id,vip_name,vip_tel_no,sex,vip_grade,birthday,remark,create_time) " \
                   "values('{0}','{1}','{3}','{4}','{5}','{6}'," \
                   "'{7}','{8}','{9}')".format(shop_id,vip_id,vip_name,vip_tel_no,sex,vip_grade,birthday,remark,date
                                                                                          )
        print(insert_sql)
