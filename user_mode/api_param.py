
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
    create_user_info={'mast_info':'telnumber,pwd,user_name','info':'telnumber,pwd,user_name'}
    #登陆/login_user
    login_user_info={'mast_info':'telnumber,pwd','info':'telnumber,pwd'}
    #忘记密码/forger_user
    forger_user_info={'mast_info':'telnumber,pwd','info':'telnumber,pwd'}
    ######查看店铺信息
    select_shop_info = {'mast_info': 'id',
                        'info': 'id,shop_id,shop_name,shop_jc,province,city,country,street,address,logo'}
    #####员工信息######
    staff_info={'mast_info': 'id','info':'shop_id,staff_id,staff_name'}