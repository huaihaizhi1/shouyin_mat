#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import re




def t_goods(request_body,path):
    mysql=PymysqlPool()
    shop_id=request_body.get('id')
    if path=='/select_goods':
        status = request_body.get('status')
        page = request_body.get('page',None)
        pageSize = request_body.get('pageSize',None)
        if page=='' or page==None or pageSize=='' or pageSize==None:
            page='1'
            pageSize = '999999999999'
        start=int(int(page)-1)*int(pageSize)
        stop=pageSize
        limit=" order by id desc limit {0}, {1}".format(start,stop)
        select_sql="select code_id,shop_id,u_code_id,goods_id,name,s_code,inventory_quantity,seling_price,unit_pinlei,unit,s_photo,min_num,threshold_remind from t_goods where shop_id='{0}' and status='{1}' " \
                   "".format(shop_id,status)
        list1=['name','start_seling_price','end_seling_price','inventory_quantity']
        tmp_sql1=""
        tmp_sql=""
        for i in request_body:
            if i in list1:
                print(request_body.get(i))
                if request_body.get(i)=='' or request_body.get(i)==None:
                    continue
                elif i=='name':
                    tmp_sql=" and (name like '%{0}%' or code_id like '%{0}%' or s_code like '%{0}% or goods_id like '%{0}%') ".format(request_body.get(i))
                elif i=='start_seling_price':
                    tmp_sql=" and seling_price >='{0}'".format(date_s_date(request_body.get(i),'GMT','day'))
                elif i=='end_seling_price':
                    tmp_sql=" and seling_price <='{0}'".format(date_s_date(request_body.get(i),'GMT','day'))
                tmp_sql1=tmp_sql1+tmp_sql
        select_sql1=select_sql+tmp_sql1+limit
        select_sql3="select count(*)  as total from t_goods where shop_id='{0}' and status='{1}' " \
                   "".format(shop_id,status)
        select_sql2=select_sql3+tmp_sql1
        print(select_sql1)
        resluts=mysql.getAll(select_sql1)
        total_sql=mysql.getAll(select_sql2)[0]['total']
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   payload=dict(page=start,
                                total=total_sql,
                                pageSize=stop,
                                pageData=resluts,
                                key='proc_id'))
    if path=='/insert_goods':
        print(request_body)
        shop_id = request_body.get('id')
        user_id = request_body.get('name')
        user_name = request_body.get('name')
        name = request_body.get('name')
        inventory_quantity = request_body.get('inventory_quantity')
        seling_price = request_body.get('seling_price')
        min_num = request_body.get('min_num')
        unit = request_body.get('unit')
        status = request_body.get('status')
        list1=['code_id','s_code','u_code','s_link','s_photo','type_id','unit_pinlei','threshold_remind']
        list2,list3=insert_sql1(list1,request_body)
        print(list2)
        print(list3)
        select_1 = "select max(goods_id) as goods_id from t_goods where shop_id='{0}'".format(shop_id)
        res111 = mysql.getAll(select_1)
        print(res111)
        if res111[0]['goods_id'] == '' or res111[0]['goods_id'] == None:
            goods_id = '10000'
        else:
            goods_id = str(int(res111[0]['goods_id'].split('_')[1]))
        print(goods_id)
        date=get_date(0,2)
        insert_sql="insert into t_goods(goods_id,shop_id,name,inventory_quantity,seling_price,min_num,unit,status,create_time,update_time" \
                   "{0}) values('{11}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',{10})".format(list2,shop_id,name,inventory_quantity,
                                                                                            seling_price,min_num,unit,status,date,date,list3),goods_id
        print(insert_sql)
        mysql.insert(insert_sql)
        #####插入流水表完成####
        insert_sql111 = "insert into t_goods_list(goods_id,shop_id,code_id,name,unit,user_id,user_name,Operation_type,create_time) values('{1}_{0}','{1}'," \
                        "'{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(goods_id, shop_id, '', name, unit,
                                                                            user_id, user_name, '进货', date)
        mysql.insert(insert_sql111)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='新增成功',
                   payload=None)
    if path=='/update_goods':
        shop_id=request_body.get('id')
        user_id=request_body.get('user_id')
        user_name=request_body.get('user_name')
        goods_id=request_body.get('goods_id')
        name=request_body.get('name')
        inventory_quantity=request_body.get('inventory_quantity','')
        min_num=request_body.get('min_num','')
        seling_price=request_body.get('seling_price','')
        type_id=request_body.get('type_id','')
        unit_pinlei=request_body.get('unit_pinlei','')
        unit=request_body.get('unit','')
        threshold_remind=request_body.get('threshold_remind','')
        code_id=request_body.get('code_id','')
        date=get_date(0,2)
        select1="select id,goods_id,shop_id,name,inventory_quantity,min_num,seling_price,type_id,unit_pinlei,unit,threshold_remind from t_goods where goods_id='{0}'".format(goods_id)
        mm1=mysql.getAll(select1)
        keys = list(mm1[0].keys())
        keys.remove('id')
        keys.remove('shop_id')
        keys.remove('goods_id')
        print(keys)
        for i in range(0,len(keys)):
            mx=mm1[0].get(keys[i])
            mx1=request_body.get(keys[i])
            if mx1==None:
                continue
            else:
                if mx!=mx1:
                    if keys[i]=='inventory_quantity':
                        insert1="insert into t_goods_inventory_flow(shop_id,code_id,goods_id,inventory_begin,inventory_after,inventory_list,create_time) values(" \
                                "'{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(shop_id,code_id,goods_id,mx,mx1,int(mx1)-int(mx),date)
                    else:
                        Operation_type='将{0}由{1}修改成{2}'.format(keys[i],mx,mx1)
                        Operation_type=re.sub('name','商品名称：',Operation_type)
                        Operation_type=re.sub('min_num','库存下线：',Operation_type)
                        Operation_type=re.sub('seling_price','销售价格：',Operation_type)
                        Operation_type=re.sub('type_id','商品分类：',Operation_type)
                        Operation_type=re.sub('unit_pinlei','商品品类：',Operation_type)
                        Operation_type=re.sub('unit','商品单位：',Operation_type)
                        Operation_type=re.sub('threshold_remind','阀值提醒：',Operation_type)
                        insert1="insert into t_goods_update_table(goods_id,shop_id,code_id,create_time,user_name,Operation_type,name) values(" \
                            "'{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(goods_id,shop_id,code_id,date,user_name,Operation_type,name)
                    print(insert1)
                    mysql.insert(insert1)
        update_sql="update t_goods set name='{0}',inventory_quantity='{1}',min_num='{2}',seling_price='{3}',type_id='{4}',unit_pinlei='{5}'," \
                   "unit='{6}',threshold_remind='{7}' where goods_id='{8}' ".format(name,inventory_quantity,min_num,seling_price,type_id,unit_pinlei,
                                                                                    unit,threshold_remind,goods_id )
        print(update_sql)
        mysql.update(update_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='修改成功',
                   payload=None)
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)

