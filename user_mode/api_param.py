
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
    create_shop={'mast_info':'id,shop_jc,shop_name,address,province,city,country,street'}
    ######查看店铺信息
    select_shop_info = {'mast_info': 'id',
                        'info': 'id,shop_id,shop_name,shop_jc,province,city,country,street,address,logo'}
    #######店铺信息修改#####
    update_shop={'mast_info':'id,shop_jc,shop_name,address,province,city,country,street,logo'}
    #######员工创建#####
    create_employess={'mast_info': 'id,staff_id,staff_name','info':'id,shop_id,staff_id,staff_name'}
    #######员工修改#####
    update_employess={'mast_info': 'id,staff_id,staff_name','info':'id,shop_id,staff_id,staff_name'}
    #####员工信息######
    staff_info={'mast_info': 'id,pageNo,pagesize','info':'id,shop_id,staff_id,staff_name'}
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
    select_purchase={'mast_info':'id,pageNo,pagesize,status','info':'id,shop_id'}
