from flask import Flask, sessions, request, make_response, jsonify
import os
from db import my_md5, PymysqlPool
from code1 import ResponseCode, ResponseMessage
import datetime
import time
server=Flask(__name__)

@server.route('/select_shop', methods=["GET","POST"])           ####登录检查########
def select_shop():
    #####获取form格式的请求体并解析
    select_shop_info = {'mast_info': 'id,shop_name',
                        'info': 'id,shop_id,shop_name,shop_jc,province,city,country,street,address'}
    request_body = request.form  # 获取接口表单参数
    aa = select_shop_info['info'].split(',')  # 逗号分隔列表
    dict={}
    for i in range(0, len(aa)):
        aa1 = request_body.get(aa[i], None)
        if aa1 != None:
            dict[aa[i]]=request_body.get(aa[i])

    return None
    telnumber=request_body.get('telnumber')
    pwd=my_md5(request_body.get('pwd'))
    payload={}
    select_sql='select telnumber,passwd,id,user_name from user_table where telnumber="%s"'%telnumber
    mysql=PymysqlPool()
    resluts=mysql.getAll(select_sql)

if __name__ == "__main__":
    server.run(port=9999, debug=True, host='0.0.0.0')

