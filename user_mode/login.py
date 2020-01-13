from flask import make_response,jsonify
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
import log
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
                                     user_name=resluts[0]['user_name'],
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
            res = dict(code=ResponseCode.FAIL,
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
        resluts=mysql.insert(insert_sql)
        if resluts==False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL-error',
                       payload=None
                       )
            msg="api:{0},error_sql:{1},sql错误".format('create_user1',insert_sql)
            log.LOG.error(msg)
            return res
        else:
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
        resluts1=mysql.update(update_sql)
        if resluts1==False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL-error',
                       payload=None
                       )
            msg="api:{0},error_sql:{1},sql错误".format('forget_user1',update_sql)
            log.LOG.error(msg)
            return res
        res = dict(code=ResponseCode.SUCCESS,
                   msg='密码修改成功',
                   payload='null')
        mysql.dispose()
    else:
        res = dict(code=ResponseCode.FAIL,
                   msg='用户未注册',
                   payload=None
                   )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
