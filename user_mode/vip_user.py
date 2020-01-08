#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import re


def vip_user(request_body, path):
    mysql=PymysqlPool()
    if path=='/insert_vipuser':
        shop_id=request_body.get('id','')
        vip_name=request_body.get('vip_name','')
        vip_tel_no=request_body.get('vip_tel_no','')
        sex=request_body.get('sex','')
        vip_grade=request_body.get('vip_grade','')
        birthday=date_s_date(request_body.get('birthday',''),'GMT','day')
        remark=request_body.get('remark','')
        date=get_date(0,2)
        select1="select max(vip_id) as vip_id from vip_table where shop_id='{0}'".format(shop_id)
        res11=mysql.getAll(select1)
        print(res11)
        if res11[0].get('vip_id')==None:
            vip_id='{0}_1001'.format(shop_id)
        else:
            vip_id='{0}_{1}'.format(shop_id,int(res11[0].get('vip_id').split('_')[1])+1)
        insert_sql="insert into vip_table(shop_id,vip_id,vip_name,vip_tel_no,sex,vip_grade,birthday,remark,create_time) " \
                   "values('{0}','{1}','{2}','{3}','{4}','{5}'," \
                   "'{6}','{7}','{8}')".format(shop_id,vip_id,vip_name,vip_tel_no,sex,vip_grade,birthday,remark,date
                                                                                          )
        print(insert_sql)
        mysql.insert(insert_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='创建成功',
                   payload=None)
    if path=='/select_vipuser':
        shop_id=request_body.get('id')
        list1 = ['vip_name', 'page']
        tmp_sql1 = ""
        limit = ''
        tmp_sql = ''
        for i in request_body:
            if i in list1:
                if request_body.get(i) == '' or request_body.get(i) == None:
                    continue
                elif i == 'vip_name':
                    tmp_sql = " and (vip_name like '%{0}%' or vip_tel_no like '%{0}%')  ".format(request_body.get(i))
                elif i == 'page':
                    page = request_body.get('page')
                    pageSize = request_body.get('pageSize')
                    start = int(int(page) - 1) * int(pageSize)
                    stop = pageSize
                    limit = " order by id desc limit {0}, {1}".format(start, stop)
                tmp_sql1 = tmp_sql1 + tmp_sql
        select_sql = " select vip_id,vip_name,vip_tel_no,sex,vip_grade,birthday,remark,code from vip_table where shop_id={0}".format(
            shop_id)
        select_sql = select_sql + tmp_sql1 + limit
        print(select_sql)
        resluts = mysql.getAll(select_sql)
        total_sql = "select count(*) as total from vip_table where shop_id={0}".format(shop_id)
        total_sql=total_sql+tmp_sql1
        if len(limit) == 0:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                       payload=dict(
                           total=mysql.getAll(total_sql)[0]['total'],
                           pageData=resluts,
                           key='vip_id'))
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                       payload=dict(page=start,
                                    total=mysql.getAll(total_sql)[0]['total'],
                                    pageSize=stop,
                                    pageData=resluts,
                                    key='vip_id'))
    if path=='/update_vipuser':
        shop_id=request_body.get('id','')
        vip_id=request_body.get('vip_id')
        vip_name=request_body.get('vip_name')
        vip_tel_no=request_body.get('vip_tel_no')
        sex=request_body.get('sex')
        vip_grade=request_body.get('vip_grade','')
        birthday=date_s_date(request_body.get('birthday',''),'GMT','day')
        remark=request_body.get('remark','')
        update_sql="update vip_table set vip_name='{0}',vip_tel_no='{1}',sex='{2}',vip_grade='{3}',birthday='{4}',remark='{5}'" \
                   " where shop_id='{6}' and vip_id='{7}'".format(vip_name,vip_tel_no,sex,vip_grade,birthday,remark,shop_id,vip_id)
        print(update_sql)
        mysql.update(update_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='修改成功',
                   payload=None)
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
