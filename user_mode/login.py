from flask import make_response,jsonify
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
##########session设置

def login_user1(request_body):
    #####获取form格式的请求体并解析
    telnumber=request_body.get('telnumber')
    pwd=my_md5(request_body.get('pwd'))
    payload={}
    select_sql='select telnumber,passwd,id,user_name from user_table where telnumber="%s"'%telnumber
    mysql=PymysqlPool()
    resluts=mysql.getAll(select_sql)
    if resluts!=[]:
        #print(list(my_db(select_sql))[0][0])
        #sessions['username']=list(my_db(select_sql))[0][0]
        if pwd==resluts[0]['passwd'] and telnumber==resluts[0]['telnumber']:
            res=dict(code=ResponseCode.SUCCESS,
                        msg=ResponseMessage.SUCCESS,
                        payload=dict(id=resluts[0]['id'],
                                     telnumber=resluts[0]['telnumber'])
                         )
            payload = dict(id=resluts[0]['id'],
                           user_name=resluts[0]['user_name'],
                           telnumber=resluts[0]['telnumber'])
            mysql.dispose()
        else:
                res=dict(code=ResponseCode.ACCOUNT_OR_PASS_WORD_ERR,
                         msg=ResponseMessage.ACCOUNT_OR_PASS_WORD_ERR,
                         payload=None
                         )
    else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户不存在',
                       payload=None
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
    mysql=PymysqlPool()
    resluts=mysql.getAll(select_sql)
    if resluts!=[]:
        res=dict(code=ResponseCode.FAIL,
                     msg='用户已存在',
                 payload=None
                     )
    else:
        insert_sql="insert into user_table(telnumber,passwd,lastday_time,user_name,create_time,update_time) values ('{0}','{1}','{2}','{3}','{4}','{5}')"\
            .format(telnumber,pwd,date,user_name,date,date)
        mysql.insert(insert_sql)
        res=dict(code=ResponseCode.SUCCESS,
                     msg='用户注册成功',
                 payload=None
                     )
        mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)


def forget_user1(request_body):
    #####获取form格式的请求体并解析
    telnumber = request_body['telnumber']
    pwd = my_md5(request_body['pwd'])
    select_sql = 'select telnumber from user_table where telnumber="%s" ' % telnumber
    mysql=PymysqlPool()
    resluts=mysql.getAll(select_sql)
    if resluts!=[]:
        update_sql = "update user_table set passwd='{0}'  where telnumber ='{1}'".format (pwd,telnumber)
        mysql.update(update_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='密码修改成功',
                   payload='null')
        mysql.dispose()
    else:
        res = dict(code=ResponseCode.SUCCESS,
                   msg='用户未注册',
                   payload=None
                   )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
