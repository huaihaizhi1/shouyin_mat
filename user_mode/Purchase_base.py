#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
import time



def purchase_goods(request_body,path):
    id=request_body.get('id')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pageNo=request_body.get('pageNo')
    pagesize=request_body.get('pagesize')
    status=request_body.get('status')
    print(request_body)
    if path=='/select_purchase':
        mysql = PymysqlPool()
        list1=['code_id','start_data','end_data','suppiler_name','price_status','start_price','end_price','purchase_no','user_name']
        select_sql="select code_id,purchase_no,purchase_date,suppiler_name,purchas_price,price_status,user_name from t_purchase_table where shop_id='{0}'".format(id)
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
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
