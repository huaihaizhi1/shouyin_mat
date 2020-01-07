#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import pandas as pd


def t_order(request_body,path):
    mysql=PymysqlPool()
    if path=='/insert_order':
        shop_id = request_body.get('id')
        staff_id = request_body.get('id','')
        vip_id = request_body.get('id','')
        pur_sal = request_body.get('pur_sal')
        pur_num = request_body.get('pur_num')
        sal = request_body.get('sal')
        Discount_type = request_body.get('Discount_type','')
        payload = request_body.get('payload')
        status = request_body.get('status')
        pay_type = request_body.get('pay_type')
        date=get_date(0,2)
        selet_get_purno_sql="select max(pur_no) as pur_no from order_master where shop_id='{0}'".format(shop_id)
        print(selet_get_purno_sql)
        res11=mysql.getOne(selet_get_purno_sql)
        print(res11)
        if res11.get('pur_no')=='' or res11.get('pur_no')==None:
            pur_no='1000001'
            pur_no=shop_id+'_'+pur_no
        else:
            pur_no=shop_id+'_'+str(int(res11.get('pur_no').split('_')[1])+1)
        ####订单表写入####
        insert_order_sql="insert into order_master(shop_id,pur_no,staff_id,vip_id,pur_sal,pur_num,create_time,status,Discount_type,sal," \
                         "pay_type) values('{0}','{1}','{2}','{3}','{4}'," \
                         "'{5}','{6}','{7}','{8}','{9}','{10}')".format(shop_id,pur_no,staff_id,vip_id,pur_sal,pur_num,date,status,Discount_type,sal,pay_type)
        print(insert_order_sql)
        res1111=mysql.insert(insert_order_sql)
        print(res1111)
        ########订单详情入库##
        print(payload)
        df=pd.DataFrame(payload)
        date=get_date(0,2)
        df['create_time']=date
        df['pur_no']=pur_no
        df=df.where(df.notnull(),None)
        print(df)
        tmp1=''
        tmp2=''
        m=0
        colume=df.columns.values.tolist()
        for i in range(0,len(colume)):
            if i==len(colume)-1:
                tmp1=tmp1+colume[i]
                tmp2=tmp2+'%s'
            else:
                tmp1=tmp1+colume[i]+','
                tmp2=tmp2+'%s'+','
        print(tmp1)
        print(tmp2)
        insert_order_detail_sql="insert into order_detail({0}) values({1})".format(tmp1,tmp2)
        tuples = [tuple(x) for x in df.values]
        print(insert_order_detail_sql)
        print(tuples)
        if mysql.insertMany(insert_order_detail_sql,tuples)==False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL error:{0}'.format(insert_order_detail_sql),
                       payload=None)
            return jsonify(res)
        else:
        #######商品流水入库####
            
        ##根据goods_id写入t_goods_list表
        #######
        res={"12":"12"}
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
