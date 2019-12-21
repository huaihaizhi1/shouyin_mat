#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *



def purchase_goods(request_body,path):
    id=request_body.get('id')
    #date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path=='/select_purchase':
        pageNo = request_body.get('pageNo')
        pagesize = request_body.get('pagesize')
        if request_body.get('start_data')=='':
            start_data=get_date(7,1)
        else:
            start_data = request_body.get('start_data')
        if request_body.get('end_data')=='':
            end_data=get_date(0,1)
        else:
            end_data = request_body.get('end_data')
        if request_body.get('start_price')=='':
            start_price='0'
        else:
            start_price = request_body.get('start_price')
        if request_body.get('end_price')=='':
            end_price='99999999999'
        else:
            end_price = request_body.get('end_price')
        mysql = PymysqlPool()
        list1=['code_id','suppiler_name','price_status','purchase_no','user_name']
        select_sql="select code_id,purchase_no,purchase_date,suppiler_name,purchas_price,price_status,user_name from t_purchase_table where shop_id='{0}'" \
                   " and purchase_date>={1} and purchase_date<={2} and purchas_price>={3} and purchas_price<={4} ".format(id,start_data,end_data,start_price,end_price)
        list2=[]
        for i in request_body:
            if i in list1:
                if request_body.get(i)!='':
                    list2.append(i)
        print(list2)
        tmp_sql1=''
        for i  in range(0,len(list2)):
            tmp_sql=" and {0}='{1}' ".format(list2[i], request_body.get(list2[i]))
            tmp_sql1=tmp_sql1+tmp_sql
        select_sql=select_sql+tmp_sql1
        start=int(int(pageNo)-1)*int(pagesize)
        stop=pagesize
        limit1=" order by id desc limit {0}, {1}".format(start,stop)
        select_sql=select_sql+limit1
        print(select_sql)
        mysql.getAll(select_sql)                         #查看货单数据####
        total_sql="select count(id) as total from t_purchase_table where shop_id='{0}'".format(id)
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   total=mysql.getAll(total_sql)[0]['total'],
                        page=start,
                   pagesize=stop,
                       payload=mysql.getAll(select_sql)
                       )
    if path=='/create_purchase':
        1
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
