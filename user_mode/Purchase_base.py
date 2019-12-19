#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,my_db
from code1 import ResponseCode,ResponseMessage
import datetime
import time



def purchase_goods(request_body,path):
    id=request_body.get('id')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pageNo=request_body.get('pageNo')
    pagesize=request_body.get('pagesize')
    print(request_body)
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
        start=int(int(pageNo)-1)*int(pagesize)
        stop=pagesize
        limit1=" order by id desc limit {0}, {1}".format(start,stop)
        select_sql=select_sql+limit1
        print(select_sql)
        my_db(select_sql)                         #查看货单数据####
        total_sql="select count(id) as total from t_purchase_table where shop_id='{0}'".format(id)
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   total=my_db(total_sql)[0]['total'],
                        page=start,
                   pagesize=stop,
                       payload=my_db(select_sql)
                       )

    if path=='/create_purchase':
        id=request_body.get('id')
        select_sql="select max(code_id) as code_id from t_purchase_table where shop_id='{0}'".format(id)
        if my_db(select_sql)[0]['code_id']=='None':
            print(my_db(select_sql))
            code1=int(my_db(select_sql)[0]['code_id'].split('_')[1])
            code_id=id+'_'+str(code1+1)
        else:
            code_id=id+'_10001'
        list1=['purchase_no','purchase_date','suppiler_no','suppiler_name','purchas_price','user_id','user_name','remarks','price_status']
        list2=[]
        for i in request_body:
            print(i, request_body.get(i))
            if i in list1:
                if request_body.get(i)=='':
                    break
                list2.append(i)
        print(list2)
        tmp_sql=''
        if len(list2)!=0:
            for i  in range(0,len(list2)):
                tmp1_sql=list2[i]
                tmp_sql=tmp1_sql+tmp_sql
            insert_sql="insert into t_purchase_table(shop_id,code_id,status,{0}) values('{1}','{2}','0',{3}) ".format(tmp_sql,id,code_id,tmp_sql)
            print(insert_sql)
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='必填项未填',
                       payload='null'
                       )

    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
