from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,my_db
from code1 import ResponseCode,ResponseMessage
import datetime
import time


def shop(request_body,path):
    #####获取form格式的请求体并解析
    id=request_body.get('id')
    shop_name=request_body.get('shop_name',None)
    shop_jc=request_body.get('shop_jc',None)
    province=request_body.get('province',None)
    city=request_body.get('city',None)
    country=request_body.get('country',None)
    street=request_body.get('street',None)
    address=request_body.get('address',None)
    logo=request_body.get('logo',None)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    select_sql = 'select shop_id,shop_jc,shop_name,address,province,city,country,logo,street from shop_base where shop_id="%s" ' % id
    insert_sql = "insert into shop_base(shop_id,shop_jc,shop_name,address,province,city,country,logo,create_time,update_time,street) " \
                 "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')" \
        .format(id, shop_jc, shop_name, address, province, city, country, logo, date, date, street)
    update_sql="update shop_base set shop_jc='{0}',shop_name='{1}',address='{2}',province='{3}',city='{4}',country='{5}',logo='{6}',update_time='{7}',street='{8}'" \
               " where  shop_id='{9}'".format( shop_jc, shop_name, address, province, city, country, logo, date, street,id)
    if path=='/create_shop':
        if my_db(select_sql):
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户已创建',
                       payload='null'
                       )
        else:
            my_db(insert_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload='null'
                       )
    if path=='/update_shop':
        if my_db(select_sql):
            my_db(update_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='修改成功',
                       payload='null'
                       )
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户未开店',
                       payload='null'
                       )
    if path=='/select_shop':
        if my_db(select_sql):
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload=my_db(select_sql)[0]
                       )
        else:
            my_db(select_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='店铺不存在',
                        payload = 'null')
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)

def staff_user(request_body,path):
    #####获取form格式的请求体并解析
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id=request_body.get('id')
    staff_id=request_body.get('staff_id',None)
    staff_name=request_body.get('staff_name',None)
    select_sql = 'select staff_id,staff_name from staff_user_table where shop_id="{0}" and status="{1}" '  .format(id,'0')
    insert_sql = "insert into staff_user_table(shop_id,staff_id,staff_name,status,create_time,update_time) " \
                 "values ('{0}','{1}','{2}','0','{3}','{4}')" \
        .format(id, staff_id, staff_name,date,date)
    update_sql="update staff_user_table set staff_name='{0}'" \
               " where  shop_id='{1}' and staff_id='{2}'".format(staff_name, id, staff_id)
    delete_sql="update staff_user_table set status='{0}'" \
               " where  shop_id='{1}' and staff_id='{2}'".format('1', id, staff_id)
    select_sql_staff_id = 'select * from staff_user_table where shop_id="{0}" and status="{1}"  and staff_id="{2}"'.format(id, '0',staff_id)
    if path=='/create_employess':
        if my_db(select_sql_staff_id):
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户已存在',
                       payload='null'
                       )
        else:
            my_db(insert_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='创建成功',
                       payload='null'
                       )
    if path=='/update_employess':
        if my_db(select_sql_staff_id):
            my_db(update_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='修改成功',
                       payload='null'
                       )
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户不存在',
                       payload='null'
                       )
    if path=='/select_employess':
        if my_db(select_sql):
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload=my_db(select_sql)
                       )
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='未添加店员',
                       payload='null')
    if path=='/delete_employess':
        if my_db(select_sql_staff_id):
            my_db(delete_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload='null'
                       )
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户不存在',
                       payload='null'
                    )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)


