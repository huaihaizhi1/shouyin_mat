from flask import make_response,jsonify
from db import my_md5,my_db
from code1 import ResponseCode,ResponseMessage
import datetime
##########session设置

def login_user1(request_body):
    #####获取form格式的请求体并解析
    telnumber=request_body.get('telnumber')
    pwd=my_md5(request_body.get('pwd'))
    payload={}
    select_sql='select telnumber,passwd,id from user_table where telnumber="%s"'%telnumber
    if my_db(select_sql):
        #print(list(my_db(select_sql))[0][0])
        #sessions['username']=list(my_db(select_sql))[0][0]
        if pwd==my_db(select_sql)[0]['passwd'] and telnumber==my_db(select_sql)[0]['telnumber']:
            res=dict(code=ResponseCode.SUCCESS,
                        msg=ResponseMessage.SUCCESS,
                        payload=dict(id=my_db(select_sql)[0]['id'],
                                     telnumber=my_db(select_sql)[0]['telnumber'])
                         )
            payload = dict(id=my_db(select_sql)[0]['id'],
                           telnumber=my_db(select_sql)[0]['telnumber'])
        else:
                res=dict(code=ResponseCode.FAIL,
                         msg='用户或者密码错误'
                         )
    else:
            res = dict(code=ResponseCode.FAIL,
                       msg='用户不存在'
                       )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res),payload

def create_user1(request_body):
    #####获取form格式的请求体并解析
    telnumber=request_body['telnumber']
    pwd=my_md5(request_body['pwd'])
    user_name=request_body['user_name']
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    select_sql = 'select telnumber from user_table where telnumber="%s" '%telnumber
    if my_db(select_sql):
        res=dict(code=ResponseCode.FAIL,
                     msg='用户已存在'
                     )
    else:
        insert_sql="insert into user_table(telnumber,passwd,lastday_time,user_name,create_time,update_time) values ('{0}','{1}','{2}','{3}','{4}','{5}')"\
            .format(telnumber,pwd,date,user_name,date,date)
        my_db(insert_sql)
        res=dict(code=ResponseCode.SUCCESS,
                     msg='用户注册成功'
                     )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)


def forget_user1(request_body):
    #####获取form格式的请求体并解析
    telnumber = request_body['telnumber']
    pwd = my_md5(request_body['pwd'])
    select_sql = 'select telnumber from user_table where telnumber="%s" ' % telnumber
    if my_db(select_sql):
        update_sql = "update user_table set passwd='{0}'  where telnumber ='{1}'".format (pwd,telnumber)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='密码修改成功')
    else:
        res = dict(code=ResponseCode.FAIL,
                   msg='用户未注册'
                   )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
