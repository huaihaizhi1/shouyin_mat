#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
import log
from db import my_md5,PymysqlPool
from code1 import ResponseCode,ResponseMessage
import datetime
from user_mode.public import *
import pandas as pd


def t_order(request_body,path):
    mysql=PymysqlPool()
    if path=='/insert_order':
        user_id=request_body.get('user_id')
        user_name = request_body.get('user_name')
        shop_id = request_body.get('id')
        if request_body.get('staff_id','')=='' or request_body.get('staff_name','')=='':
            staff_id=user_id
            staff_name=user_name
        else:
            staff_id=request_body.get('staff_id')
            staff_name=request_body.get('staff_name')
        vip_id = request_body.get('vip_id','')
        pur_sal = request_body.get('pur_sal')
        pur_num = request_body.get('pur_num')
        sal = request_body.get('sal')
        Discount_type = request_body.get('Discount_type','')
        payload = request_body.get('payload')
        status = request_body.get('status')
        pay_type = request_body.get('pay_type')

        date=get_date(0,2)
        selet_get_purno_sql="select max(pur_no) as pur_no from order_master where shop_id='{0}'".format(shop_id)
        print(selet_get_purno_sql)
        res11=mysql.getOne(selet_get_purno_sql)
        print(res11)
        if res11.get('pur_no')=='' or res11.get('pur_no')==None:
            pur_no='1000001'
            pur_no=str(shop_id)+'_'+pur_no
        else:
            pur_no=str(shop_id)+'_'+str(int(res11.get('pur_no').split('_')[1])+1)
        ####订单表写入####
        print(staff_id)
        insert_order_sql="insert into order_master(shop_id,pur_no,staff_id,vip_id,pur_sal,pur_num,create_time,status,Discount_type,sal," \
                         "pay_type) values('{0}','{1}','{2}','{3}','{4}'," \
                         "'{5}','{6}','{7}','{8}','{9}','{10}')".format(shop_id,pur_no,staff_id,vip_id,pur_sal,pur_num,date,status,Discount_type,sal,pay_type)
        print(insert_order_sql)
        res1111=mysql.insert(insert_order_sql)
        if res1111==False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL-error',
                       payload=None
                       )
            msg="api:{0},error_sql:{1},sql错误".format(path,insert_order_sql)
            log.LOG.error(msg)
            return res
        #######积分增加#######
        if vip_id!='' or vip_id!=None:
            ins_vip_code="update vip_table set code=(case when code is null then 0 else code end)+{0} where vip_id='{1}'".format(sal,vip_id)
            print(ins_vip_code)
            m10=mysql.update(ins_vip_code)
            if m10 == False:
                res = dict(code=ResponseCode.FAIL,
                           msg='SQL-error',
                           payload=None
                           )
                msg = "api:{0},error_sql:{1},sql错误,积分增加".format(path, ins_vip_code)
                log.LOG.error(msg)
                return res
        ########订单详情入库##
        print(payload)
        df=pd.DataFrame(payload)
        date=get_date(0,2)
        df['create_time']=date
        df['pur_no']=pur_no
        df=df.where(df.notnull(),None)
        print(df)
        tmp1=''
        tmp2=''
        m=0
        colume=df.columns.values.tolist()
        for i in range(0,len(colume)):
            if i==len(colume)-1:
                tmp1=tmp1+colume[i]
                tmp2=tmp2+'%s'
            else:
                tmp1=tmp1+colume[i]+','
                tmp2=tmp2+'%s'+','
        insert_order_detail_sql="insert into order_detail({0}) values({1});".format(tmp1,tmp2)
        tuples = [tuple(x) for x in df.values]
        print(tuples)
        if mysql.insertMany(insert_order_detail_sql,tuples)==False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL error:',
                       payload=None)
            log.LOG.error("订单详情插入错误。sql:{0}".format(insert_order_detail_sql))
            return jsonify(res)
        else:
            for tmpdict in payload:
                insert_goods_list="insert into t_goods_list(goods_id,shop_id,code_id,name,unit,user_id,user_name,Operation_type,create_time,pur_no,status) values(" \
                                  "'{0}','{1}','{2}'," \
                                  "'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(tmpdict.get('goods_id'),
                                                                                      tmpdict.get('shop_id'),
                                                                                      tmpdict.get('code_id'),
                                                                                      tmpdict.get('name'),
                                                                                      tmpdict.get('count'),
                                                                                      staff_id,
                                                                                      staff_name,'销售',
                                                                                      date,pur_no,'0'
                                                                                      )
                print(insert_goods_list)
                update_t_goods_sql="update t_goods set inventory_quantity=inventory_quantity-{0} where goods_id='{1}'".format(tmpdict.get('count'),tmpdict.get('goods_id'))
                print(update_t_goods_sql)
                m1=mysql.insert(insert_goods_list) ###流水入库##
                if m1 == False:
                    res = dict(code=ResponseCode.FAIL,
                               msg='SQL-error',
                               payload=None
                               )
                    msg = "api:{0},error_sql:{1},sql错误,流水入库".format(path, insert_goods_list)
                    log.LOG.error(msg)
                    return res
                m2=mysql.update(update_t_goods_sql)###库存处理
                if m2 == False:
                    res = dict(code=ResponseCode.FAIL,
                               msg='SQL-error',
                               payload=None
                               )
                    msg = "api:{0},error_sql:{1},sql错误,库存处理".format(path, update_t_goods_sql)
                    log.LOG.error(msg)
                    return res
        res = dict(code=ResponseCode.SUCCESS,
                   msg='数据处理成功',
                   payload=None)
    if path == '/select_order':
        shop_id = request_body.get('id')
        pur_no = request_body.get('pur_no')
        select1="select pur_no,create_time from order_master where shop_id='{0}' and pur_no='{1}'".format(shop_id,pur_no)
        select2="select id as proc_id,shop_id,goods_id,name,number,seling_price,price_num,s_code,u_code from order_detail where shop_id='{0}' and pur_no='{1}'".format(shop_id,pur_no)
        print(select1)
        print(select2)
        re111=mysql.getOne(select1)
        re222=mysql.getAll(select2)
        res = dict(code=ResponseCode.SUCCESS,
                       msg='查询成功',
                   payload=dict(pur_no=re111.get('pur_no'),
                                create_time=re111.get('create_time'),
                                pageData=re222,
                                key='proc_id'))
    if path == '/del_order':
        shop_id = request_body.get('id')
        del_pur_no = request_body.get('pur_no')
        staff_id = request_body.get('staff_id')
        vip_id = request_body.get('vip_id')
        pur_sal = request_body.get('pur_sal')
        pur_num = request_body.get('pur_num')
        status = request_body.get('status')
        sal = request_body.get('sal')
        pay_type = request_body.get('pay_type')
        payload = request_body.get('payload')
        staff_name = request_body.get('staff_name')
        date=get_date(0,2)
        selet_get_purno_sql="select max(pur_no) as pur_no from order_master where shop_id='{0}'".format(shop_id)
        print(selet_get_purno_sql)
        res11=mysql.getOne(selet_get_purno_sql)
        print(res11)
        if res11.get('pur_no')=='' or res11.get('pur_no')==None:
            pur_no='1000001'
            pur_no=str(shop_id)+'_'+pur_no
        else:
            pur_no=str(shop_id)+'_'+str(int(res11.get('pur_no').split('_')[1])+1)
        ins_order_mast="insert into order_master(shop_id,pur_no,staff_id,vip_id,pur_sal,pur_num,create_time,status,sal,del_pur_no,pay_type) " \
                       "values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(
            shop_id,pur_no,staff_id,vip_id,pur_sal,pur_num,date,status,sal,del_pur_no,pay_type
        )
        print(ins_order_mast)
        res1111 = mysql.insert(ins_order_mast)
        if res1111==False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL-error',
                       payload=None
                       )
            msg="api:{0},error_sql:{1},sql错误".format(path,ins_order_mast)
            log.LOG.error(msg)
            return res        #######积分扣减#######
        if vip_id!='' or vip_id!=None:
            ins_vip_code="update vip_table set code=(case when code is null then 0 else code end)-{0} where vip_id='{1}'".format(sal,vip_id)
            m2=mysql.update(ins_vip_code)
            if m2 == False:
                res = dict(code=ResponseCode.FAIL,
                           msg='SQL-error',
                           payload=None
                           )
                msg = "api:{0},error_sql:{1},sql错误".format(path, ins_vip_code)
                log.LOG.error(msg)
                return res
        ########订单详情入库##
        print(payload)
        df = pd.DataFrame(payload)
        date = get_date(0, 2)
        df['create_time'] = date
        df['pur_no'] = pur_no
        df = df.where(df.notnull(), None)
        print(df)
        tmp1 = ''
        tmp2 = ''
        m = 0
        colume = df.columns.values.tolist()
        for i in range(0, len(colume)):
            if i == len(colume) - 1:
                tmp1 = tmp1 + colume[i]
                tmp2 = tmp2 + '%s'
            else:
                tmp1 = tmp1 + colume[i] + ','
                tmp2 = tmp2 + '%s' + ','
        insert_order_detail_sql = "insert into order_detail({0}) values({1})".format(tmp1, tmp2)
        tuples = [tuple(x) for x in df.values]
        print(insert_order_detail_sql)
        print(tuples)
        if mysql.insertMany(insert_order_detail_sql, tuples) == False:
            res = dict(code=ResponseCode.FAIL,
                       msg='SQL error:{0}'.format(insert_order_detail_sql),
                       payload=None)
            return jsonify(res)
        else:
            for tmpdict in payload:
                insert_goods_list = "insert into t_goods_list(goods_id,shop_id,code_id,name,unit,user_id,user_name,Operation_type,create_time,pur_no,status) values(" \
                                    "'{0}','{1}','{2}'," \
                                    "'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(tmpdict.get('goods_id'),
                                                                                        tmpdict.get('shop_id'),
                                                                                        tmpdict.get('code_id'),
                                                                                        tmpdict.get('name'),
                                                                                        tmpdict.get('count'),
                                                                                        staff_id,
                                                                                        staff_name, '退货',
                                                                                        date, pur_no,'1'
                                                                                        )
                print(insert_goods_list)
                update_t_goods_sql = "update t_goods set inventory_quantity=inventory_quantity+{0} where goods_id='{1}'".format(
                    tmpdict.get('count'), tmpdict.get('goods_id'))
                print(update_t_goods_sql)
                m4=mysql.insert(insert_goods_list)  ###流水入库##
                if m4 == False:
                    res = dict(code=ResponseCode.FAIL,
                               msg='SQL-error',
                               payload=None
                               )
                    msg = "api:{0},error_sql:{1},sql错误".format(path, insert_goods_list)
                    log.LOG.error(msg)
                    return res
                m5=mysql.update(update_t_goods_sql)  ###库存处理
                if m5 == False:
                    res = dict(code=ResponseCode.FAIL,
                               msg='SQL-error',
                               payload=None
                               )
                    msg = "api:{0},error_sql:{1},sql错误".format(path, update_t_goods_sql)
                    log.LOG.error(msg)
                    return res
        res = dict(code=ResponseCode.SUCCESS,
                   msg='数据处理成功',
                   payload=None)
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
