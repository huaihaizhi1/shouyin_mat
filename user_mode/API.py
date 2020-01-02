from user_mode.login import *
from user_mode.public import *
from user_mode.shop_base import *
from user_mode.api_param import api_param
from flask import Flask, session, request
import os
from user_mode.Purchase_base import *
from user_mode.t_goods import *



server=Flask(__name__)
server.config['JSON_AS_ASCII'] = False
server.config['SECRET_KEY'] = os.urandom(24)
# @server.before_request#执行所有装饰器都要执行当前装饰器(简洁版实现同样功能)
# def login_required():
#     if request.path in ['/create_user','/forget_user','/testGetCaptcha','/login_user']: #如果登录的路由是注册和登录就返会none
#         return None
#     user=session.get('telnumber')  #获取用户登录信息
#     if not user:                 #没有登录就自动跳转到登录页面去
#         res={"code":401,
#              "msg":"未登录",
#              "payload":""}
#         return res
#     return None
@server.route("/login_user",methods=["POST","GET"])                  #用户登陆
def login_user():                                                       #注意接口名称与上面相同
    dict1=api_param.login_user1                                     #获取接口参数必填项与参数列表(需要修改)
    request_body=request.form                                           #获取接口表单参数
    res1=Required_verification(request_body,dict1)
    if res1['code']==200:         #必填项检查是否为200
        session['telnumber'] = request_body.get('telnumber')
        res,payload=login_user1(request_body)                                  #必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
        session['payload'] = payload
    else:
        res=res1                   #接口返回不为200则提示错误系信息
    return res

@server.route("/create_user",methods=["POST","GET"])                #用户注册
def create_user():
    dict1=api_param.create_user1                                     #获取接口参数必填项与参数列表
    request_body=request.form                                           #获取接口表单参数
    Required_verification(request_body,dict1)                           #接口必填项验证
    scode=session.get("code")
    if test_verify_captcha(request_body,scode)['code'] !=200:
        return test_verify_captcha(request_body,scode)
    if Required_verification(request_body,dict1)['code']==200:         #必填项检查是否为200
        session['telnumber'] = request_body.get('telnumber')
        res=create_user1(request_body)                                  #必填项为200则进入接口执行阶段并返回结果
    else:
        res=Required_verification(request_body,dict1)                   #接口返回不为200则提示错误系信息
    return res

@server.route("/forget_user",methods=["POST","GET"])                #忘记密码
def forget_user():
    dict1=api_param.forget_user1                                     #获取接口参数必填项与参数列表
    request_body=request.form                                           #获取接口表单参数
    if Required_verification(request_body,dict1)['code']==200:         #必填项检查是否为200
        res=forget_user1(request_body)                                  #必填项为200则进入接口执行阶段并返回结果
    else:
        res=Required_verification(request_body,dict1)                   #接口返回不为200则提示错误系信息
    return res
@server.route("/login_out",methods=["POST","GET"])                #退出登录
def login_out():
    session.clear()
    res = dict(code=ResponseCode.SUCCESS,
               msg='登出成功'
               )
    return res

@server.route('/testGetCaptcha', methods=["GET"])           ####图片验证码获取########
def test_get_captcha():
    """
    获取图形验证码
    :return:
    """
    new_captcha = CaptchaTool()
    # 获取图形验证码
    img, code = new_captcha.get_verify_code()
    # 存入session
    session["code"] = code
    res={"code":200,
         "msg":'成功获取图片',
         "payload":{"url":img.decode()}}
    return res
@server.route('/login_check', methods=["GET"])           ####登陆验证########
def login_check():
    user=session.get('telnumber')  #获取用户登录信息
    payload = session.get('payload')
    res = {"code": 200,
           "msg": "已登录",
           "payload": payload}
    if not user:                 #没有登录就自动跳转到登录页面去
        res={"code":401,
             "msg":"未登录",
             "payload":""}
    return res
@server.route('/create_shop',methods=["POST","GET"])           ####创建开店信息########
def create_shop():
    dict1 = api_param.create_shop  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = shop(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/select_shop',methods=["POST","GET"])           ####查看开店信息########
def select_shop():
    dict1 = api_param.select_shop_info  # 获取接口参数必填项与参数列表(需要修改)
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = shop(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/update_shop',methods=["POST","GET"])           ####修改开店信息########
def update_shop():
    dict1 = api_param.update_shop  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = shop(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/create_employess',methods=["POST","GET"])           ####新增店员########
def create_employess():
    dict1 = api_param.create_employess  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = staff_user(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/update_employess',methods=["POST","GET"])           ####修改店员信息########
def update_employess():
    dict1 = api_param.update_employess  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = staff_user(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/select_employess',methods=["POST","GET"])           ####查看店员信息########
def select_employess():
    dict1 = api_param.staff_info  # 获取接口参数必填项与参数列表(需要修改)
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = staff_user(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/delete_employess',methods=["POST","GET"])           ####删除店员信息########
def delete_employess():
    dict1 = api_param.delete_employess  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = staff_user(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res


@server.route('/select_catalog',methods=["POST","GET"])           ####查看分类信息########
def select_catalog():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_catalog  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = catalog(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/update_catalog',methods=["POST","GET"])           ####修改分类信息信息########
def update_catalog():
    dict1 = api_param.update_catalog  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = catalog(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/del_catalog',methods=["POST","GET"])           ####删除分类信息########
def del_catalog():
    dict1 = api_param.del_catalog  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = catalog(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/create_catalog',methods=["POST","GET"])           ####创建分类信息########
def create_catalog():
    dict1 = api_param.create_catalog  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = catalog(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res
@server.route('/province',methods=["POST","GET"])           ####查看省份信息########
def province():
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res = total_address(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    return res
@server.route('/city',methods=["POST","GET"])           ####查看城市信息########
def city():
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res = total_address(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    return res
@server.route('/area',methods=["POST","GET"])           ####查看地区分类信息########
def area():
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res = total_address(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    return res

@server.route('/select_purchase',methods=["POST","GET"])           ####查看货单列表########
def select_purchase():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_purchase  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = purchase_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/create_purchase',methods=["POST","GET"])           ####查看货单列表########
def create_purchase():
    if request.method=='POST':
        request_body = request.get_json(force=True)  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.create_purchase  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = purchase_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res


@server.route('/select_purchase_pro1',methods=["POST","GET"])           ####查看货单详情_基本信息查看########
def select_purchase_pro1():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_purchase_pro  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = purchase_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/select_purchase_pro2',methods=["POST","GET"])           ####查看货单详情_商品信息查看########
def select_purchase_pro2():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_purchase_pro  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = purchase_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/select_purchase_pro3',methods=["POST","GET"])           ####查看货单详情_操作日志查看########
def select_purchase_pro3():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_purchase_pro  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = purchase_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res


@server.route('/update_purchase',methods=["POST","GET"])           ####货单修改########
def update_purchase():
    dict1 = api_param.update_purchase  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = purchase_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/select_supplier',methods=["POST","GET"])           ####查看供应商信息########
def select_supplier():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_supplier  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = supplier_api(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res


@server.route('/update_supplier',methods=["POST","GET"])           ####修改供应商########
def update_supplier():
    dict1 = api_param.update_supplier  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = supplier_api(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res


@server.route('/delete_supplier',methods=["POST","GET"])           ####删除供应商########
def delete_supplier():
    dict1 = api_param.delete_supplier  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = supplier_api(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/insert_supplier',methods=["POST","GET"])           ####新增供应商########
def insert_supplier():
    dict1 = api_param.insert_supplier  # 获取接口参数必填项与参数列表(需要修改)
    request_body = request.form  # 获取接口表单参数
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = supplier_api(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/select_goods',methods=["POST","GET"])           ####新增供应商########
def select_goods():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.select_goods  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = t_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

@server.route('/insert_goods',methods=["POST","GET"])           ####新增供应商########
def insert_goods():
    if request.method=='POST':
        request_body = request.form  # 获取接口表单参数
    elif request.method=='GET':
        request_body = request.args
    dict1 = api_param.insert_goods  # 获取接口参数必填项与参数列表(需要修改)
    path=request.path
    res1 = Required_verification(request_body, dict1)
    if res1['code'] == 200:  # 必填项检查是否为200
        res = t_goods(request_body,path)  # 必填项为200则进入接口执行阶段并返回结果(注意接口地址变化)
    else:
        res = res1  # 接口返回不为200则提示错误系信息
    return res

