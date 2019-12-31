#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import json




def t_goods(request_body,path):
    mysql=PymysqlPool()
    shop_id=request_body.get('id')
    if path=='/select_goods':
        page = request_body.get('page')
        status = request_body.get('status')
        pageSize = request_body.get('pageSize')
        start=int(int(page)-1)*int(pageSize)
        stop=pageSize
        limit=" order by id desc limit {0}, {1}".format(start,stop)
        select_sql="select name,s_code,inventory_quantity,seling_price,unit_pinlei,unit,s_photo,min_num,threshold_remind from t_goods where shop_id='{0}' and status='{1}' " \
                   "".format(shop_id,status)
        list1=['name','start_seling_price','end_seling_price','inventory_quantity']
        tmp_sql1=""
        tmp_sql=""
        for i in request_body:
            if i in list1:
                print(request_body.get(i))
                if request_body.get(i)=='' or request_body.get(i)==None:
                    continue
                elif i=='name':
                    tmp_sql=" and (name like '%{0}%' or code_id like '%{0}%' or s_code like '%{0}%') ".format(request_body.get(i))
                elif i=='start_seling_price':
                    tmp_sql=" and seling_price >='{0}'".format(request_body.get(i))
                elif i=='end_seling_price':
                    tmp_sql=" and seling_price <='{0}'".format(request_body.get(i))
                tmp_sql1=tmp_sql1+tmp_sql
        select_sql1=select_sql+tmp_sql1+limit
        print(select_sql1)
        resluts=mysql.getAll(select_sql1)
        total_sql=len(resluts)
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   payload=dict(page=start,
                                total=total_sql,
                                pageSize=stop,
                                pageData=resluts,
                                key='proc_id'))
    if path=='/insert_goods':
        print(request_body)
        shop_id = request_body.get('id')
        name = request_body.get('name')
        inventory_quantity = request_body.get('inventory_quantity')
        seling_price = request_body.get('seling_price')
        min_num = request_body.get('min_num')
        unit = request_body.get('unit')
        status = request_body.get('status')
        list1=['code_id','s_code','u_code','s_link','s_photo','type_id','unit_pinlei','threshold_remind']
        list2,list3=insert_sql1(list1,request_body)
        print(list2)
        print(list3)
        date=get_date(0,2)
        insert_sql="insert into t_goods(shop_id,name,inventory_quantity,seling_price,min_num,unit,status,create_time,update_time," \
                   "{0}) values('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',{10})".format(list2,shop_id,name,inventory_quantity,
                                                                                            seling_price,min_num,unit,status,date,date,list3)
        print(insert_sql)
        mysql.insert(insert_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='新增成功',
                   payload=None)
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)

