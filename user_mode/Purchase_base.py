#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *



def purchase_goods(request_body,path):
    id=request_body.get('id')
    #date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path=='/select_purchase':
        pageNo = request_body.get('pageNo')
        pagesize = request_body.get('pagesize')
        if request_body.get('start_data')=='':
            start_data=get_date(7,1)
        else:
            start_data = request_body.get('start_data')
        if request_body.get('end_data')=='':
            end_data=get_date(0,1)
        else:
            end_data = request_body.get('end_data')
        if request_body.get('start_price')=='' or request_body.get('start_price')==None:
            start_price='0'
        else:
            start_price = request_body.get('start_price')
        if request_body.get('end_price')=='' or request_body.get('end_price')==None:
            end_price='99999999999'
        else:
            end_price = request_body.get('end_price')
        mysql = PymysqlPool()
        list1=['code_id','suppiler_name','price_status','purchase_no','user_name']
        select_sql="select code_id,purchase_no,purchase_date,suppiler_name,purchas_price,price_status,user_name from t_purchase_table where shop_id='{0}'" \
                   " and purchase_date>={1} and purchase_date<={2} and purchas_price>={3} and purchas_price<={4} ".format(id,start_data,end_data,start_price,end_price)
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
    if path=='/create_purchase':
        mysql=PymysqlPool()
        ########必填项#########
        shop_id = request_body.get('id')
        purchase_date = request_body.get('purchase_date')
        purchas_price = request_body.get('purchas_price')
        user_id = request_body.get('id')
        user_name = request_body.get('user_name')
        price_status = request_body.get('price_status')
        payload = request_body.get('payload')
        ###非必填项########
        #####货单编号生成#####
        select_sql="select max(code_id) as code_id from t_purchase_table where shop_id={0}".format(shop_id)
        res111=mysql.getAll(select_sql)
        if res111[0]['code_id']==None:
            code_id = user_id+'_10001'
        else:
            tmp_id=str(int(res111[0]['code_id'].split('_')[1])+1)
            code_id=user_id+'_'+tmp_id
        print(code_id)
        purchase_no=request_body.get('purchase_no')
        if purchase_no=='' or purchase_no==None:
            purchase_no = 'MAX9999'
        suppiler_name=request_body.get('suppiler_name')
        if suppiler_name=='' or suppiler_name==None:
            suppiler_name = '默认供应商'
        suppiler_no=request_body.get('suppiler_no')
        if suppiler_no==''or suppiler_no==None:
            suppiler_no = '-1'
        remarks=request_body.get('remarks')
        insert_sql="insert into t_purchase_table(shop_id,code_id,purchase_no,purchase_date,suppiler_no,suppiler_name,purchas_price,status," \
                   "user_id,user_name,remarks,price_status) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')" \
                   "".format(shop_id,code_id,purchase_no,purchase_date,suppiler_no,suppiler_name,purchas_price,'0',user_id,user_name,remarks,price_status)
        print(insert_sql)
        mysql.insert(insert_sql)
        if payload=='' or payload==None or payload==[]:
            ########货单流水记录##########
            date = get_date(0, 1)
            insert_tmp_sql="insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type) values('{0}','{1}','{2}',{3}," \
                           "'{4}','{5}')".format(shop_id,code_id,date,user_name,'创建')
            insert_tmp1_sql="insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type) values('{0}','{1}','{2}',{3}," \
                           "'{4}','{5}')".format(shop_id,code_id,date,user_name,'确认')
            mysql.insert(insert_tmp_sql)
            mysql.insert(insert_tmp1_sql)
            ################
            mysql.dispose()
            res = dict(code=ResponseCode.SUCCESS,
                       msg='货单创建成功，未添加商品',
                       payload=None
                       )
        else:
            print(payload)
            for i in range(0,len(payload)):
                shop_id=payload['payload']
                code_id=code_id
                s_code=payload['s_code']
                u_code=payload['u_code']
                s_link=payload['s_link']
                s_photo=payload['s_photo']
                name=payload['name']
                inventory_quantity=payload['inventory_quantity']
                min_num=payload['min_num']
                seling_price=payload['seling_price']
                type_id=payload['type_id']
                unit_pinlei=payload['unit_pinlei']
                unit=payload['unit']
                threshold_remind=payload['threshold_remind']
                insert_sql="insert into t_goods()"
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)



def supplier_api(request_body,path):
    mysql = PymysqlPool()
    if path=='/select_supplier':
        shop_id=request_body.get('id')
        pageNo = request_body.get('pageNo')
        pagesize = request_body.get('pagesize')
        start=int(int(pageNo)-1)*int(pagesize)
        stop=pagesize
        name=request_body.get('name')
        select_sql=" select name,number,address,contact,last_act_date,remarks from t_supplier where shop_id={0} and status='0'}".format(shop_id,)
        limit1=" order by id desc limit {0}, {1}".format(start,stop)
        if name=='' or name==None:
            select_sql=select_sql+limit1
        else:
            select_sql = " select id as proc_id,name,number,address,contact,last_act_date,remarks from t_supplier where shop_id={0} and ststus='0' and name like '%{1}%'".format(
                shop_id,name)
            select_sql=select_sql+limit1
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        total_sql="select count(*) as total from t_supplier where shop_id={0} and status='0'".format(shop_id)
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   total=mysql.getAll(total_sql)[0]['total'],
                        page=start,
                   pagesize=stop,
                       payload=resluts
                       )
    if path=='/update_supplier':
        shop_id=request_body.get('id')
        name=request_body.get('name')
        number=request_body.get('number')
        address=request_body.get('address')
        contact=request_body.get('contact')
        proc_id=request_body.get('proc_id')
        remarks=request_body.get('remarks')
        update_sql="update t_supplier set name='{0}' , number='{1}' , address='{2}' , contact='{3}'" \
                   " , remarks='{4}'  where shop_id='{5}' and id='{6}'".format(name,number,address,contact,remarks,shop_id,proc_id)
        print(update_sql)
        mysql.update(update_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='修改成功',
                   payload=None
                   )
    if path=='/delete_supplier':
        proc_id=request_body.get('proc_id')
        shop_id=request_body.get('id')
        delete_sql="update t_supplier set status='1' where id='{0}' and shop_id='{1}'".format(proc_id,shop_id)
        print(delete_sql)
        mysql.update(delete_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='删除成功',
                   payload=None
                   )
    if path=='/insert_supplier':
        shop_id=request_body.get('id')
        name=request_body.get('name')
        number=request_body.get('number')
        address=request_body.get('address')
        contact=request_body.get('contact')
        remarks=request_body.get('remarks')
        date=get_date(0,2)
        insert_sql="insert into t_supplier(shop_id,name,number,address,contact,remarks,status,create_time) values" \
                   "('{0}','{1}','{2}','{3}','{4}','{5}','0','{6}')".format(shop_id,name,number,address,contact,remarks,date)
        print(insert_sql)
        mysql.insert(insert_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='新增成功',
                   payload=None
                   )
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return res
