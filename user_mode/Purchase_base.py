#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,my_db
from code1 import ResponseCode,ResponseMessage
import datetime
import time



def purchase_goods(request_body,path):
    id=request_body.get('id')
    code_id=request_body.get('code_id',None)
    purchase_no=request_body.get('purchase_no',None)
    purchase_date=request_body.get('purchase_date',None)
    suppiler_no=request_body.get('suppiler_no',None)
    suppiler_name=request_body.get('suppiler_name',None)
    purchas_price=request_body.get('purchas_price',None)
    user_id=request_body.get('user_id',None)
    user_name=request_body.get('user_name',None)
    remarks=request_body.get('remarks',None)
    price_status=request_body.get('price_status',None)
    goods=request_body.get('goods',None)
    print(request_body)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path=='/select_purchase':
        list1=['code_id','purchase_date','suppiler_name','price_status','goods','purchas_price','user_name']
        select_sql="select code_id,purchase_no,purchase_date,suppiler_name,purchas_price,price_status,user_name from t_purchase_table"
        tem_sql=' where '
        print(select_sql)