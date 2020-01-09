#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *




def Management(request_body,path):
    mysql=PymysqlPool()
    if path=='/bi_Business_analysis':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        print(start_date)
        select_sql="select date,	"\
                    "sum(sal1) as '销售金额',	"\
                    "sum(sal2) as '交易笔数',	"\
                    "sum(sal3) as '退货金额',	"\
                    "sum(sal4) as '进货金额',	"\
                    "sum(sal5) as '销售商品数量'	"\
                    "from 	"\
                    "(select 	"\
                    "	 1 as type,	"\
                    "	date(create_time) AS date,	"\
                    "	sum(case  when status=0 then sal ELSE 0 end) sal1,	"\
                    "	sum(case  when status=0 then 1 ELSE 0 end) sal2,	"\
                    "	sum(case  when status=1 then sal ELSE 0 end) sal3, 	"\
                    "	0 sal4,	"\
                    "	0 sal5	"\
                    "FROM	"\
                    "	order_master where shop_id='{0}' and create_time BETWEEN '{1}' and '{2}'	"\
                    "group by date(create_time)	"\
                    "union all	"\
                    "SELECT	"\
                    "	 2 as type,	"\
                    "	 	purchase_date as date,	"\
                    "	0 as sal1,	"\
                    "	0 as sal2,	"\
                    "	0 as sal3,	"\
                    "	sum(purchase_price) as sal4,	"\
                    "		0 as sal5	"\
                    "FROM	"\
                    "	t_purchase_table where shop_id='{0}' and create_time BETWEEN '{1}' and '{2}'	"\
                    "GROUP BY	"\
                    "	purchase_date	"\
                    "union all	"\
                    "SELECT	"\
                    "	 3 as type,	"\
                    "	date(create_time) AS date,	"\
                    "	0 as sal1,	"\
                    "	0 as sal2,	"\
                    "	0 as sal3,	"\
                    "	0 as sal4,	"\
                    "	count(DISTINCT goods_id) as sal5	"\
                    "FROM	"\
                    "	order_detail WHERE STATUS = 0 	"\
                    " and shop_id='{0}' and create_time BETWEEN '{1}' and '{2}'	"\
                    ") as t group by t.date	".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        print(resluts)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                                pageData=resluts,
                                key='date'))
    if path=='/bi_Business_sum':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        goods_id=request_body.get('goods_id','')
        if goods_id!='' and goods_id!=None:
            select_sql="select date(create_time) date ,	"\
                        "sum(case  when status=0 then seling_price*number ELSE 0 end) as '销售额',	"\
                        "sum(seling_price)/count(seling_price) as '日均单价',	"\
                        "sum(case  when status=0 then number ELSE 0 end) as '销售数量',	"\
                        "sum(case  when status=1 then number ELSE 0 end) as '退货数量',	"\
                        "sum(case  when status=1 then seling_price*number ELSE 0 end) as '退货额'	"\
                        " from order_detail	"\
                        "where shop_id='{0}'   and create_time BETWEEN '{1}' and '{2}' and goods_id='{3}'	"\
                        "group by date(create_time)	".format(shop_id,start_date,end_date,goods_id)
        else:
            select_sql="select date(create_time) date ,sum(case  when status=0 then sal ELSE 0 end) sal1 as '营销额'," \
                       "sum(case  when status=1 then sal ELSE 0 end) sal2 as '退货额'  "\
                        "from  order_master where shop_id='{0}'   and create_time BETWEEN '{1}' and '{2}' "\
                        "group by date(create_time) ".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                                pageData=resluts,
                                key='date'))
    if path == '/bi_Business_goods':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        select_sql="select goods_id,	"\
                "name,	"\
                "sum(seling_price)/count(number) as '售价',	"\
                "sum(case  when status=0 then seling_price*number ELSE 0 end) as '销售额',	"\
                "sum(case  when status=0 then number ELSE 0 end) as '销量',	"\
                "sum(case  when status=1 then seling_price*number ELSE 0 end) as '退货额',	"\
                "sum(case  when status=1 then number ELSE 0 end) as '退货量'	"\
                "from order_detail where shop_id='{0}'   and create_time BETWEEN '{1}' and '{2}'	"\
                "group by goods_id,name	".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                                pageData=resluts,
                                key='date'))
    if path == '/bi_Business_goods_list':
        111
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
