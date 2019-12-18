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
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path=='/select_purchase':
        list1=['code_id','purchase_date','suppiler_name','price_status','goods','purchas_price','user_name']
        select_sql="select code_id,purchase_no,purchase_date,suppiler_name,purchas_price,price_status,user_name from t_purchase_table where shop_id='{0}'".format(id)
        list2=[]
        for i in request_body:
            print(i, request_body.get(i))
            if i in list1:
                list2.append(i)
        tmp_sql1=''
        for i  in range(0,len(list2)):
            tmp_sql=" and {0}='{1}' ".format(list2[i], request_body.get(list2[i]))
            tmp_sql1=tmp_sql1+tmp_sql
        select_sql=select_sql+tmp_sql1
        print(select_sql)
        my_db(select_sql)                         #查看货单数据####
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                       payload=my_db(select_sql)
                       )

    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
