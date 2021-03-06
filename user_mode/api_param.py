import decimal
import flask.json
class api_param(object):
    #######接口参数验证##########
    ######mastinfo是必填项#######
    ######info是接口所有参数#####
    # 所有参数json格式
    # 基础模块：
    # 用户管理
    #     注册 /create_user
    #         参数：telnumber,pwd,user_name
    #     登录 /login_user
    #         参数:telnumber,pwd
    #     忘记密码 /forget_user
    #         参数:telnumber,pwd
    #店铺信息/create_shop /select_shop /update_shop
    #       参数：  id 登录ID
    #               shop_name 店铺名称
    #
    #注册/create_user
    create_user1={'mast_info':'telnumber,pwd,user_name','info':'telnumber,pwd,user_name'}
    #登陆/login_user
    login_user1={'mast_info':'telnumber,pwd','info':'telnumber,pwd'}
    #忘记密码/forger_user
    forget_user1={'mast_info':'telnumber,pwd','info':'telnumber,pwd'}
    ########创建店铺######
    create_shop={'mast_info':'id,shop_jc,shop_name,address,province,city,area'}
    ######查看店铺信息
    select_shop_info = {'mast_info': 'id',
                        'info': 'id,shop_id,shop_name,shop_jc,province,city,area,address'}
    #######店铺信息修改#####
    update_shop={'mast_info':'id,shop_jc,shop_name,address,province,city,area'}
    #######员工创建#####
    create_employess={'mast_info': 'id,staff_id,staff_name','info':'id,shop_id,staff_id,staff_name'}
    #######员工修改#####
    update_employess={'mast_info': 'id,staff_id,staff_name','info':'id,shop_id,staff_id,staff_name'}
    #####员工信息######
    staff_info={'mast_info': 'id','info':'id,shop_id,staff_id,staff_name'}
    #######员工删除#####
    delete_employess={'mast_info': 'id,staff_id','info':'id,shop_id,staff_id,staff_name'}
    #######商品分类查看####
    select_catalog={'mast_info':'id','info':'id,shop_id'}
    #######商品分类修改####
    update_catalog={'mast_info':'id,name,s_id','info':'id,shop_id'}
    #######商品分类查看####
    del_catalog={'mast_info':'id,s_id','info':'id,shop_id'}
    #######商品分类查看####
    create_catalog={'mast_info':'id,name,s_id','info':'id,shop_id'}
    ###货单主页查询###########
    select_purchase={'mast_info':'id,page,pageSize','info':'id,shop_id'}
    ######货单新增###########
    create_purchase={'mast_info':'id,purchase_date,purchas_price,user_id,user_name,price_status,payload'}
    #####查看货单详情#####
    select_purchase_pro={'mast_info':'id,code_id'}

    #####货单修改#####
    update_purchase={'mast_info':'id,code_id,status,purchase_price,price_status,user_name'}
    ##########供应商查看####
    select_supplier={'mast_info':'id'}
    #######供应商修改#######
    update_supplier={'mast_info':'id,name,number,address,proc_id'}
    ######供应商删除########
    delete_supplier={'mast_info':'id,proc_id'}
    ######供应商添加########
    insert_supplier={'mast_info':'id,name'}
    ######商品查看#########
    select_goods={'mast_info':'id,status'}
    ######商品写入########
    insert_goods={'mast_info':'id,inventory_quantity,name,seling_price,min_num,unit,status,user_name,user_id'}
    ######商品修改########
    update_goods={'mast_info':'id,goods_id,name,inventory_quantity,min_num,seling_price,user_name,user_id'}
    ######会员新增########
    insert_vipuser={'mast_info':'id,vip_name,vip_tel_no,birthday'}
    ######会员查看########
    select_vipuser={'mast_info':'id'}
    ######会员修改########
    update_vipuser={'mast_info':'id,vip_id,vip_name,vip_tel_no'}
    ######销售下单########
    insert_order={'mast_info':'id,pur_sal,pur_num,sal,payload,status,pay_type'}
    ######订单查询########
    select_order={'mast_info':'id,pur_no'}
    ######退货处理########
    del_order={'mast_info':'id,pur_no,staff_id,staff_name,pur_sal,pur_num,sal,payload,status,pay_type,pur_no'}
    ######经营分析########
    bi_Business_analysis={'mast_info':'id,start_date,end_date'}
    ######销售查询########
    bi_Business_sum={'mast_info':'id,start_date,end_date'}
    ######商品销售排行########
    bi_Business_goods={'mast_info':'id,start_date,end_date'}
    ######商品流水查看########
    bi_Business_goods_list={'mast_info':'id,goods_id'}
    ######未销售商品查询########
    bi_Business_goods_1={'mast_info':'id,start_date,end_date'}
    ######商品修改记录########
    bi_goods_update_list1={'mast_info':'id,start_date,end_date'}
    ######商品库存调整记录########
    bi_goods_update_list2={'mast_info':'id,start_date,end_date'}
    ######导购员业绩查询########
    bi_staff_select={'mast_info':'id,start_date,end_date'}
    ######应付账款查询########
    t_supplier_put={'mast_info':'id'}
    ######付款接口########
    t_supplier_get={'mast_info':'id,code_id,unpay_price,user_name,user_id,pay_price'}
    ######shouye########
    bi_shouye={'mast_info':'id'}

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)