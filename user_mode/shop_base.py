from flask import Flask,sessions,request,make_response,jsonify
import os
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
import time


def shop(request_body,path):                                ######店铺管理##########
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
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql)
        if resluts:                           #查看店铺是否存在
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户已创建',
                       payload='null'
                       )
        else:
            mysql.insert(insert_sql)                           #店铺创建
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload='null'
                       )
            mysql.dispose()
    if path=='/update_shop':
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql)
        if resluts:                       #查看店铺是否存在
            mysql.update(update_sql)                       #修改店铺信息
            res = dict(code=ResponseCode.SUCCESS,
                       msg='修改成功',
                       payload='null'
                       )
            mysql.dispose()
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户未开店',
                       payload='null'
                       )
    if path=='/select_shop':
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql)
        if resluts:                       #查看店铺是否存在并返回店铺数据
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload=resluts[0]
                       )
            mysql.dispose()
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='店铺不存在',
                        payload = 'null')
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)

def staff_user(request_body,path):                  #####导购员管理########
    #####获取form格式的请求体并解析
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id=request_body.get('id')
    staff_id=request_body.get('staff_id',None)
    staff_name=request_body.get('staff_name',None)
    pageNo=request_body.get('pageNo')
    pagesize=request_body.get('pagesize')
    select_sql = 'select staff_id,staff_name from staff_user_table where shop_id="{0}" and status="{1}" '.format(id,'0')
    insert_sql = "insert into staff_user_table(shop_id,staff_id,staff_name,status,create_time,update_time) " \
                 "values ('{0}','{1}','{2}','0','{3}','{4}')" \
        .format(id, staff_id, staff_name,date,date)
    update_sql="update staff_user_table set staff_name='{0}'" \
               " where  shop_id='{1}' and staff_id='{2}'".format(staff_name, id, staff_id)
    delete_sql="update staff_user_table set status='{0}'" \
               " where  shop_id='{1}' and staff_id='{2}'".format('1', id, staff_id)
    select_sql_staff_id = 'select * from staff_user_table where shop_id="{0}" and status="{1}"  and staff_id="{2}"'.format(id, '0',staff_id)
    if path=='/create_employess':               #创建店员####
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql_staff_id)
        if resluts:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户已存在',
                       payload='null'
                       )
        else:
            mysql.insert(insert_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='创建成功',
                       payload='null'
                       )
            mysql.dispose()
    if path=='/update_employess':
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql_staff_id)
        if resluts:
            mysql.update(update_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='修改成功',
                       payload='null'
                       )
            mysql.dispose()
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户不存在',
                       payload='null'
                       )
    if path=='/select_employess':
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql)
        if resluts:
            start = int(int(pageNo) - 1) * int(pagesize)
            stop = pagesize
            limit1 = " order by id desc limit {0}, {1}".format(start, stop)
            select_sql = select_sql + limit1
            print(select_sql)
            total_sql = "select count(id) as total from staff_user_table where shop_id='{0}' and status=0".format(id)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       total=mysql.getAll(total_sql)[0]['total'],
                       page=start,
                       pagesize=stop,
                       payload=resluts
                       )
            mysql.dispose()
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='未添加店员',
                       payload='null')
    if path=='/delete_employess':
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql_staff_id)
        if resluts:
            mysql.update(delete_sql)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='操作成功',
                       payload='null'
                       )
            mysql.dispose()
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户不存在',
                       payload='null'
                    )
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)

def catalog(request_body,path):                         #######商品分类管理##########
    id=request_body.get('id')
    name=request_body.get('name')
    s_id=request_body.get('s_id')
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if path=='/select_catalog':
        select_sql="select id,CONCAT(id,CONCAT('_'),gradeid)  s_id,name from Catalog_table where shop_id='{0}' and gradeid=1 ".format(id)
        mysql = PymysqlPool()
        resluts = mysql.getAll(select_sql)
        if resluts:
            tmp_list2=[]
            for st1 in mysql.getAll(select_sql):
                #print(st1)
                select_sql = "select id,CONCAT(id,CONCAT('_'),gradeid)  s_id,name from Catalog_table where shop_id='{0}' and piarentid='{1}' ".format(id,st1['id'])
                #print(my_db(select_sql))
                tmp_list1=[]
                for st2 in mysql.getAll(select_sql):
                    select_sql = "select id,CONCAT(id,CONCAT('_'),gradeid)  s_id,name from Catalog_table where shop_id='{0}' and piarentid='{1}' ".format(id,st2['id'])
                    data=(mysql.getAll(select_sql))
                    st2['children']=data
                    tmp_list1.append(st2)
                st1['children'] = tmp_list1
                tmp_list2.append(st1)
            print(tmp_list2)
            res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                       payload=tmp_list2
                    )
        else:
            res = dict(code=ResponseCode.SUCCESS,
                       msg='用户未分类',
                       payload='null'
                    )
        mysql.dispose()
    elif path=='/update_catalog':
        s_id=s_id.split('_')
        select_sql="select id from Catalog_table where shop_id='{0}' and id='{1}'".format(id,s_id[0])
        mysql = PymysqlPool()
        if mysql.getAll(select_sql):
            update_sql="update Catalog_table set name='{0}' where shop_id='{1}' and id='{2}' ".format(name,id,s_id[0])
            mysql.update(update_sql)
            res = dict(code=ResponseCode.SUCCESS,
               msg='修改成功',
               payload='null'
               )
        else:
            res = dict(code=ResponseCode.SUCCESS,
               msg='id不存在',
               payload='null'
               )
        mysql.dispose()
    elif path=='/del_catalog':
        s_id=s_id.split('_')
        select_sql="select id from Catalog_table where gradeid='{0}' and id='{1}' and shop_id='{2}'"\
                        "union ALL "\
                        "select id from Catalog_table where  piarentid in (select id from Catalog_table "\
                        "where gradeid='{0}' and id='{1}' and shop_id='{2}'"\
                        ")"\
                        "union all "\
                        "select id from  Catalog_table where  piarentid   in "\
                        "(select id from Catalog_table where  piarentid in "\
                        "(select id from Catalog_table "\
                        "where gradeid='{0}' and id='{1}' and shop_id='{2}'"\
                        "))".format(s_id[1],s_id[0],id)
        st2=''
        mysql = PymysqlPool()
        for i in range(0,len(mysql.getAll(select_sql))):
            if i==len(mysql.getAll(select_sql))-1:
                st2=st2+str(mysql.getAll(select_sql)[i]['id'])
            else:
                st2=st2+str(mysql.getAll(select_sql)[i]['id'])+','
        del_sql="delete from Catalog_table where id in ({0}) and shop_id='{1}'".format(st2,id)
        mysql.delete(del_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='删除成功',
                   payload='null'
                   )
        mysql.dispose()
    elif path=='/create_catalog':
        mysql = PymysqlPool()
        if s_id=='-1':
            insert_sql="insert into Catalog_table(shop_id,name,gradeid,piarentid,status,create_time,update_time) " \
                   "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(id,name,'1','0','0',date,date)
        else:
            s_id = s_id.split('_')
            gradeid=int(s_id[1])+1
            piarentid=s_id[0]
            insert_sql="insert into Catalog_table(shop_id,name,gradeid,piarentid,status,create_time,update_time) " \
                   "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(id,name,gradeid,piarentid,'0',date,date)
        mysql.insert(insert_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='创建成功',
                   payload='null'
                   )
        mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)

