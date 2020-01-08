#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
from user_mode.api_param import api_param



def purchase_goods(request_body,path):
    id=request_body.get('id')
    #date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path=='/select_purchase':
        shop_id=request_body.get('id')
        page = request_body.get('page',None)
        pageSize = request_body.get('pageSize',None)
        if page=='' or page==None:
            page='1'
        if pageSize=='' or pageSize==None:
            pageSize='999999999999'
        start=int(int(page)-1)*int(pageSize)
        stop=pageSize
        limit=" order by id desc limit {0}, {1}".format(start,stop)
        list1=['code_id','suppiler_name','price_status','start_price','end_price','user_name','status']
        tmp_sql1=""
        tmp_sql=""
        for i in request_body:
            if i in list1:
                if request_body.get(i)=='':
                    continue
                elif request_body.get(i)=='-1':
                    continue
                elif i=='code_id':
                    tmp_sql=" and (code_id like '%{0}%' or purchase_no like '%{0}%')".format(request_body.get(i))
                elif i=='start_price':
                    tmp_sql=" and purchase_price >={0}".format(request_body.get(i))
                elif i=='end_price':
                    tmp_sql=" and purchase_price <={0}".format(request_body.get(i))
                elif i=='start_date':
                    tmp_sql=" and purchase_date >={0}".format(date_s_date(request_body.get(i),'GMT','day'))
                elif i=='end_date':
                    tmp_sql=" and purchase_date <={0}".format(date_s_date(request_body.get(i),'GMT','day'))
                else:
                    tmp_sql = " and {0}='{1}' ".format(i, request_body.get(i))
                tmp_sql1=tmp_sql1+tmp_sql
        print(tmp_sql1)
        select_sql="select id as proc_id,code_id,purchase_no,purchase_date,suppiler_name,purchase_price,price_status,status,user_name from t_purchase_table where shop_id='{0}'".format(shop_id)
        select_sql=select_sql+tmp_sql1
        select_sql=select_sql+limit
        mysql = PymysqlPool()
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        total_sql="select count(*) total  from t_purchase_table where shop_id='{0}'".format(shop_id)
        total_sql=total_sql+tmp_sql1
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   payload=dict(page=start,
                                total=mysql.getAll(total_sql)[0]['total'],
                                pageSize=stop,
                                pageData=resluts,
                                key='proc_id'))
        mysql.dispose()
    if path=='/create_purchase':
        mysql=PymysqlPool()
        ########必填项#########
        shop_id = request_body.get('id')
        print(request_body.get('purchase_date'))
        print(type(request_body.get('purchase_date')))
        purchase_date =date_s_date(request_body.get('purchase_date'), 'Z', 'day')
        purchase_price = request_body.get('purchase_price')
        user_id = request_body.get('id')
        user_name = request_body.get('user_name')
        price_status = request_body.get('price_status')
        payload = request_body.get('payload')
        ###非必填项########
        #####货单编号生成#####
        select_sql="select max(code_id) as code_id from t_purchase_table where shop_id={0}".format(shop_id)
        res111=mysql.getAll(select_sql)
        if res111[0]['code_id']==None:
            code_id = str(user_id)+'_10001'
        else:
            tmp_id=str(int(res111[0]['code_id'].split('_')[1])+1)
            code_id=str(user_id)+'_'+tmp_id
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
        date=get_date(0,2)
        insert_sql="insert into t_purchase_table(shop_id,code_id,purchase_no,purchase_date,suppiler_no,suppiler_name,purchase_price,status," \
                   "user_id,user_name,remarks,price_status,create_time) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')" \
                   "".format(shop_id,code_id,purchase_no,purchase_date,suppiler_no,suppiler_name,purchase_price,'0',user_id,user_name,remarks,price_status,date)
        print(insert_sql)
        mysql.insert(insert_sql)
        ########货单流水记录##########
        insert_tmp_sql = "insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type) values('{0}','{1}','{2}','{3}'," \
                         "'{4}')".format(shop_id, code_id, date, user_name, '创建')
        insert_tmp1_sql = "insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type) values('{0}','{1}','{2}','{3}'," \
                          "'{4}')".format(shop_id, code_id, date, user_name, '确认')
        mysql.insert(insert_tmp_sql)
        mysql.insert(insert_tmp1_sql)
        ################
        if payload=='' or payload==None or payload==[]:
            mysql.dispose()
            res = dict(code=ResponseCode.SUCCESS,
                       msg='货单创建成功，未添加商品',
                       payload=None
                       )
        else:
            #####商品插入流程##############
            print(payload)
            #new_s = payload.replace('cnt_"r0x_ratio"', '"cnt_r0x_ratio"')
            #ls = eval(new_s)
            aa = api_param.insert_goods
            aa1 = aa['mast_info'].split(',')  # 逗号分隔必填项列表
            aa1.remove('id')
            aa1.remove('status')
            aa1.remove('user_name')
            aa1.remove('user_id')
            print(aa1)
            shop_id = request_body.get('id')
            print(shop_id)
            select_1="select max(goods_id) as goods_id from t_goods where shop_id='{0}'".format(shop_id)
            res111 = mysql.getAll(select_1)
            print(res111)
            if res111[0]['goods_id'] == '' or res111[0]['goods_id']==None:
                goods_id = '10000'
            else:
                goods_id = str(int(res111[0]['goods_id'].split('_')[1]))
            print(goods_id)
            for i in range(0,len(payload)):
                keys = list(payload[i].keys())
                for j in aa1:
                    if j not in keys:
                        res = dict(code=ResponseCode.FAIL,
                                   msg='第{0}行参数{1}必填项未填'.format(i,j),
                                   payload=None
                                   )
                        return res
                goods_id=int(goods_id)+1
                code_id=code_id
                s_code=payload[i].get('s_code','')
                u_code=payload[i].get('u_code','')
                s_link=payload[i].get('s_link','')
                s_photo=payload[i].get('s_photo','')
                name=payload[i].get('name')
                inventory_quantity=payload[i].get('inventory_quantity','')
                min_num=payload[i].get('min_num','')
                seling_price=payload[i].get('seling_price','')
                type_id=payload[i].get('type_id','')
                unit_pinlei=payload[i].get('unit_pinlei','')
                unit=payload[i].get('unit','')
                threshold_remind=payload[i].get('threshold_remind','')
                status=payload[i].get('status','0')
                ####货单商品新增######
                date = get_date(0, 1)
                insert_sql="insert into t_goods(shop_id,code_id,s_code,u_code,s_link,s_photo,name," \
                           "inventory_quantity,min_num,seling_price,type_id,unit_pinlei,unit,threshold_remind,status,goods_id,create_time,update_time) values('{0}','{1}'," \
                           "'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{0}_{15}','{16}','{17}')".format(
                    shop_id,code_id,s_code,u_code,s_link,s_photo,name,inventory_quantity,min_num,seling_price,type_id
                    ,unit_pinlei,unit,threshold_remind,status,goods_id,date,date)
                mysql.insert(insert_sql)
                ####查看直接查询流水表t_goods_list####
                insert_sql111="insert into t_goods_list(goods_id,shop_id,code_id,name,unit,user_id,user_name,Operation_type,create_time) values('{1}_{0}','{1}'," \
                              "'{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(goods_id,shop_id,code_id,name,unit,user_id,user_name,'进货',date)
                mysql.insert(insert_sql111)
            mysql.dispose()
            res = dict(code=ResponseCode.SUCCESS,
                       msg='货单创建成功，成功添加商品',
                       payload=None
                       )
    if path=='/select_purchase_pro1':             ###查看货单详情_基本信息查看
        shop_id = request_body.get('id')
        code_id = request_body.get('code_id')
        #page = request_body.get('page')
        #pageSize = request_body.get('pageSize')
        #start=int(int(page)-1)*int(pageSize)
        #stop=pageSize
        #limit=" order by id desc limit {0}, {1}".format(start,stop)
        mysql=PymysqlPool()
        select_sql_1="select code_id,shop_id,purchase_no,purchase_date,suppiler_name,purchase_price,price_status,remarks from t_purchase_table where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        select_sql_2="select id,name,inventory_quantity,seling_price,type_id,unit_pinlei,unit from t_goods where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        select_sql_3="select id,user_name,create_time,Operation_type,remarks from  t_purchase_flow where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        m1=mysql.getAll(select_sql_1)
        print(select_sql_1)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='货单详情查看_基本信息',
                   payload=dict(pageData=m1[0],
                                key='code_id')
                   )
        ######货单数据展现还要继续参考，未完成##
        mysql.dispose()
    if path=='/select_purchase_pro2':             ###查看货单详情_基本信息查看
        shop_id = request_body.get('id')
        code_id = request_body.get('code_id')
        page = request_body.get('page')
        pageSize = request_body.get('pageSize')
        start=int(int(page)-1)*int(pageSize)
        stop=pageSize
        limit=" order by id desc limit {0}, {1}".format(start,stop)
        mysql=PymysqlPool()
        #select_sql_1="select code_id,shop_id,purchase_no,purchase_date,suppiler_name,purchase_price,remarks from t_purchase_table where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        select_sql_2="select id as l,name,inventory_quantity,seling_price,type_id,unit_pinlei,unit from t_goods where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        #select_sql_3="select id,user_name,create_time,Operation_type,remarks from  t_purchase_flow where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        resluts=mysql.getAll(select_sql_2+limit)
        print(select_sql_2+limit)
        print(resluts)
        select_sql_2="select count(*) as total from t_goods where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='操作成功',
                   payload=dict(page=start,
                                total=mysql.getAll(select_sql_2)[0]['total'],
                                pageSize=stop,
                                pageData=resluts,
                                key='proc_id'))
        ######货单数据展现还要继续参考，未完成##
        mysql.dispose()
    if path=='/select_purchase_pro3':             ###查看货单详情_基本信息查看
        shop_id = request_body.get('id')
        code_id = request_body.get('code_id')
        page = request_body.get('page')
        pageSize = request_body.get('pageSize')
        start=int(int(page)-1)*int(pageSize)
        stop=pageSize
        limit=" order by id desc limit {0}, {1}".format(start,stop)
        mysql=PymysqlPool()
        #select_sql_1="select code_id,shop_id,purchase_no,purchase_date,suppiler_name,purchase_price,remarks from t_purchase_table where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        #select_sql_2="select id as proc_id,name,inventory_quantity,seling_price,type_id,unit_pinlei,unit from t_goods where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        select_sql_3="select id,user_name,create_time,Operation_type,remarks from  t_purchase_flow where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        resluts=mysql.getAll(select_sql_3+limit)
        print(select_sql_3+limit)
        print(resluts)
        select_sql_3="select count(*) as total from t_purchase_flow where code_id='{0}' and shop_id='{1}'".format(code_id,shop_id)
        print(select_sql_3)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='操作成功',
                   payload=dict(page=start,
                                total=mysql.getAll(select_sql_3)[0]['total'],
                                pageSize=stop,
                                pageData=resluts,
                                key='proc_id'))
        ######货单数据展现还要继续参考，未完成##
        mysql.dispose()
    if path=='/update_purchase':
        mysql=PymysqlPool()
        date = get_date(0, 0)
        shop_id=request_body.get('id')
        code_id=request_body.get('code_id')
        status=request_body.get('status')
        purchase_price=request_body.get('purchase_price')
        print(purchase_price)
        price_status=request_body.get('price_status')
        user_name=request_body.get('user_name')
        remarks=request_body.get('remarks')
        ######查询修改参数记录流水############
        select_sql="select status,purchase_price,price_status from t_purchase_table where shop_id='{0}' and code_id='{1}'".format(shop_id,code_id)
        print(mysql.getAll(select_sql))
        rrr=mysql.getAll(select_sql)
        update_purchase_sql="update t_purchase_table set status='{0}',purchase_price='{1}',price_status='{2}'  where shop_id='{3}' and code_id='{4}'".format(
            status,purchase_price,price_status,shop_id,code_id)
        mysql.update(update_purchase_sql)
        if str(status)!=str(rrr[0]['status']) and str(rrr[0]['status'])=='0':
            #####货单流水修改####
            insert_sql="insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type,remarks) values('{0}','{1}','{2}'," \
                       "'{3}','{4}','{5}')".format(shop_id,code_id,date,user_name,'作废(商品信息删除)',remarks)
            mysql.insert(insert_sql)
            ########作废后商品数据修改#######
            insert_sql1="update t_goods set status=1 where shop_id='{0}' and code_id='{1}'".format(shop_id,code_id)
            mysql.insert(insert_sql1)
        if str(purchase_price)!=str(rrr[0]['purchase_price']):
            ########商品金额修改
            mt='金额由{0}修改为{1}'.format(rrr[0]['purchase_price'],purchase_price)
            insert_sql="insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type,remarks) values('{0}','{1}','{2}'," \
                       "'{3}','{4}','{5}')".format(shop_id,code_id,date,user_name,mt,remarks)
            mysql.insert(insert_sql)
        if str(price_status)!=str(rrr[0]['price_status']):
            ########商品金额修改
            if str(price_status)=='1':
                insert_sql="insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type,remarks) values('{0}','{1}','{2}'," \
                       "'{3}','{4}','{5}')".format(shop_id,code_id,date,user_name,'修改成未付款',remarks)
                mysql.insert(insert_sql)
            if str(price_status)=='0':
                insert_sql="insert into t_purchase_flow(shop_id,code_id,create_time,user_name,Operation_type,remarks) values('{0}','{1}','{2}'," \
                       "'{3}','{4}','{5}')".format(shop_id,code_id,date,user_name,'修改成已付款',remarks)
                mysql.insert(insert_sql)
        mysql.dispose()
        res = dict(code=ResponseCode.SUCCESS,
                   msg='货单修改成功',
                   payload=None
                   )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)



def supplier_api(request_body,path):
    mysql = PymysqlPool()
    if path=='/select_supplier':
        shop_id=request_body.get('id')
        list1=['name','page']
        tmp_sql1=""
        limit=''
        tmp_sql=''
        for i in request_body:
            if i in list1:
                if request_body.get(i)=='' or request_body.get(i)==None:
                    continue
                elif i=='name':
                    tmp_sql=" and (name like '%{0}%' or contact like '%{0}%' or number like '%{0}%' )".format(request_body.get(i))
                elif i=='page':
                    page = request_body.get('page')
                    pageSize = request_body.get('pageSize')
                    start = int(int(page) - 1) * int(pageSize)
                    stop = pageSize
                    limit = " order by id desc limit {0}, {1}".format(start, stop)
                tmp_sql1=tmp_sql1+tmp_sql
        select_sql=" select id as proc_id,name,number,address,contact,last_act_date,remarks from t_supplier where shop_id={0} and status='0'".format(shop_id)
        select_sql=select_sql+tmp_sql1+limit
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        total_sql="select count(*) as total from t_supplier where shop_id={0} and status='0'".format(shop_id)
        if len(limit)==0:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                       payload=dict(
                                    total=mysql.getAll(total_sql)[0]['total'],
                                    pageData=resluts,
                                    key='proc_id'))
        else:
            res = dict(code=ResponseCode.SUCCESS,
                           msg='查询成功',
                        payload = dict(page=start,
                           total=mysql.getAll(total_sql)[0]['total'],
                           pageSize=stop,
                           pageData=resluts,
                           key='proc_id'))
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
        if mysql.update(delete_sql)==False:
            res=dict(code=ResponseCode.FAIL,
                   msg='sqlcuowu',
                   payload=delete_sql
                   )
        else:
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
