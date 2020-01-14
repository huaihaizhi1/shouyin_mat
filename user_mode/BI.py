#-*-coding:utf-8-*-
from flask import Flask,sessions,request,make_response,jsonify
from db import my_md5,PymysqlPool
from user_mode.public import *




def Management(request_body,path):
    mysql=PymysqlPool()
    if path=='/bi_Business_analysis':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        print(start_date)
        select_sql="select date,	"\
                    "sum(sal1) as '销售金额',	"\
                    "sum(sal2) as '交易笔数',	"\
                    "sum(sal3) as '退货金额',	"\
                    "sum(sal4) as '进货金额',	"\
                    "sum(sal5) as '销售商品数量'	"\
                    "from 	"\
                    "(select 	"\
                    "	 1 as type,	"\
                    "	date(create_time) AS date,	"\
                    "	sum(case  when status=0 then sal ELSE 0 end) sal1,	"\
                    "	sum(case  when status=0 then 1 ELSE 0 end) sal2,	"\
                    "	sum(case  when status=1 then sal ELSE 0 end) sal3, 	"\
                    "	0 sal4,	"\
                    "	0 sal5	"\
                    "FROM	"\
                    "	order_master where shop_id='{0}' and create_time BETWEEN '{1}' and '{2}'	"\
                    "group by date(create_time)	"\
                    "union all	"\
                    "SELECT	"\
                    "	 2 as type,	"\
                    "	 	purchase_date as date,	"\
                    "	0 as sal1,	"\
                    "	0 as sal2,	"\
                    "	0 as sal3,	"\
                    "	sum(purchase_price) as sal4,	"\
                    "		0 as sal5	"\
                    "FROM	"\
                    "	t_purchase_table where shop_id='{0}' and create_time BETWEEN '{1}' and '{2}'	"\
                    "GROUP BY	"\
                    "	purchase_date	"\
                    "union all	"\
                    "SELECT	"\
                    "	 3 as type,	"\
                    "	date(create_time) AS date,	"\
                    "	0 as sal1,	"\
                    "	0 as sal2,	"\
                    "	0 as sal3,	"\
                    "	0 as sal4,	"\
                    "	count(DISTINCT goods_id) as sal5	"\
                    "FROM	"\
                    "	order_detail WHERE STATUS = 0 	"\
                    " and shop_id='{0}' and create_time BETWEEN '{1}' and '{2}'	"\
                    ") as t group by t.date	".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        print(resluts)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                                pageData=resluts,
                                key='date'))
    if path=='/bi_Business_sum':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        goods_id=request_body.get('goods_id','')
        if goods_id!='' and goods_id!=None:
            select_sql="select date(create_time) date ,	"\
                        "sum(case  when status=0 then seling_price*number ELSE 0 end) as '销售额',	"\
                        "sum(seling_price)/count(seling_price) as '日均单价',	"\
                        "sum(case  when status=0 then number ELSE 0 end) as '销售数量',	"\
                        "sum(case  when status=1 then number ELSE 0 end) as '退货数量',	"\
                        "sum(case  when status=1 then seling_price*number ELSE 0 end) as '退货额'	"\
                        " from order_detail	"\
                        "where shop_id='{0}'   and create_time BETWEEN '{1}' and '{2}' and goods_id='{3}'	"\
                        "group by date(create_time)	".format(shop_id,start_date,end_date,goods_id)
        else:
            select_sql="select date(create_time) date ,sum(case  when status=0 then sal ELSE 0 end) sal1 as '营销额'," \
                       "sum(case  when status=1 then sal ELSE 0 end) sal2 as '退货额'  "\
                        "from  order_master where shop_id='{0}'   and create_time BETWEEN '{1}' and '{2}' "\
                        "group by date(create_time) ".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                                pageData=resluts,
                                key='date'))
    if path == '/bi_Business_goods':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        select_sql="select goods_id,	"\
                "name,	"\
                "sum(seling_price)/count(number) as '售价',	"\
                "sum(case  when status=0 then seling_price*number ELSE 0 end) as '销售额',	"\
                "sum(case  when status=0 then number ELSE 0 end) as '销量',	"\
                "sum(case  when status=1 then seling_price*number ELSE 0 end) as '退货额',	"\
                "sum(case  when status=1 then number ELSE 0 end) as '退货量'	"\
                "from order_detail where shop_id='{0}'   and create_time BETWEEN '{1}' and '{2}'	"\
                "group by goods_id,name	".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts=mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                                pageData=resluts,
                                key='date'))
    if path == '/bi_Business_goods_list':
        shop_id=request_body.get('id')
        goods_id=request_body.get('goods_id')
        select="select id as proc_id,goods_id,code_id,Operation_type,pur_no,name,unit from t_goods_list  where shop_id='{0}' and goods_id='{1}'".format(shop_id,goods_id)
        print(select)
        resluts = mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                       pageData=resluts,
                       key='proc_id'))
    if path == '/bi_Business_goods_1':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        select="select id as proc_id,m.goods_id,code_id,s_code,name,inventory_quantity,seling_price from t_goods m,	"\
                    "(select goods_id from "\
                    "(select goods_id,"\
                    "sum(case  when Operation_type='销售' then 1 ELSE 0 end) as m1"\
                    "from t_goods_list  where shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}'"\
                    "	group by goods_id) y where y.m1=0) t"\
                    "where t.goods_id=m.goods_id".format(shop_id,start_date,end_date)
        print(select)
        resluts = mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                       pageData=resluts,
                       key='proc_id'))
    if path == '/bi_goods_update_list1':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        goods_id=request_body.get('goods_id')
        if goods_id!='' or goods_id!=None:
            select_sql="select id as proc_id,goods_id,name,Operation_type,user_name	"\
                        " from t_goods_update_table   "\
                        " where shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}' and goods_id='{3}' ".format(shop_id,start_date,end_date,goods_id)
        else:
            select_sql="select id as proc_id,goods_id,name,Operation_type,user_name	"\
                        " from t_goods_update_table   "\
                        " where shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}' ".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts = mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                       pageData=resluts,
                       key='proc_id'))
    if path == '/bi_goods_update_list2':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        goods_id=request_body.get('goods_id')
        if goods_id!='' or goods_id!=None:
            select_sql="select pro_id as proc_id,goods_id,name,code_id,inventory_begin,inventory_after,inventory_list,	"\
                        "user_id,user_name	"\
                        " from t_goods_inventory_flow  	"\
                        "  where shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}' and goods_id='{3}'	".format(shop_id,start_date,end_date,goods_id)
        else:
            select_sql="select pro_id as proc_id,goods_id,name,code_id,inventory_begin,inventory_after,inventory_list,	"\
                        "user_id,user_name	"\
                        " from t_goods_inventory_flow  	"\
                        "  where shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}'".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts = mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                       pageData=resluts,
                       key='proc_id'))
    if path == '/bi_staff_select':
        shop_id=request_body.get('id')
        start_date=date_s_date(request_body.get('start_date'),'GMT','get')
        end_date=date_s_date(request_body.get('end_date'),'GMT','get')
        staff_id=request_body.get('staff_id')
        if goods_id!='' or goods_id!=None:
            select_sql="select id as proc_id, m.staff_id,staff_name,t.营销额,t.销售数量 from staff_user_table m,	"\
                            "(select staff_id,	"\
                            "sum(case  when status=0 then pur_num ELSE 0 end)  as '销售数量',	"\
                            "sum(case  when status=0 then sal ELSE 0 end)  as '营销额' 	"\
                            "from order_master  where staff_id !='' and staff_id is not null	"\
                            "	 and shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}' and staff_id='{3}'	"\
                            "	 group by staff_id) t where m.staff_id=t.staff_id	".format(shop_id,start_date,end_date,staff_id)
        else:
            select_sql="select id as proc_id, m.staff_id,staff_name,t.营销额,t.销售数量 from staff_user_table m,	"\
                            "(select staff_id,	"\
                            "sum(case  when status=0 then pur_num ELSE 0 end)  as '销售数量',	"\
                            "sum(case  when status=0 then sal ELSE 0 end)  as '营销额' 	"\
                            "from order_master  where staff_id !='' and staff_id is not null	"\
                            "	 and shop_id='{0}'  and create_time BETWEEN '{1}' and '{2}' "\
                            "	 group by staff_id) t where m.staff_id=t.staff_id	".format(shop_id,start_date,end_date)
        print(select_sql)
        resluts = mysql.getAll(select_sql)
        res = dict(code=ResponseCode.SUCCESS,
                   msg='查询成功',
                   payload=dict(
                       pageData=resluts,
                       key='proc_id'))
    mysql.dispose()
    resp = make_response(res)
    resp.headers['Content-Type'] = 'text/json'
    return jsonify(res)
