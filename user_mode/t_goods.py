#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import json




def t_goods(request_body,path):
    mysql=PymysqlPool
    shop_id=request_body.get('id')
    if path=='/select_goods':
        pageNo = request_body.get('pageNo')
        pagesize = request_body.get('pagesize')
        select_sql="select name,s_code,inventory_quantity,seling_price,unit_pinlei,unit,s_photo,min_num,threshold_remind from t_goods where shop_id='{0}'".format(shop_id)


