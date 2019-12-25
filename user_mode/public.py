from code1 import *
from datetime import datetime, date
from datetime import timedelta
##############################必填项检查#########################
def Required_verification(request_body,dict1):       ###必填项检查
    if request_body:                                    #判断接口是否有参数
        canshu=dict1                                    #获取接口参数列表
        aa=canshu['mast_info'].split(',')             #逗号分隔必填项列表
        m=0                                             #用于判断必填项是否都填了
        str=''                                          #用于错误信息提示
        for i in range(0,len(aa)):                      #循环判断必填项检查
            if request_body.get(aa[i]) or request_body.get(aa[i])!='':                 #检查必填字段
                m=m+1                                    #用于验证必填
            else:
                str=str+aa[i]+','                       #错误信息提示
        if m==len(aa):
            res=dict(code=ResponseCode.SUCCESS,
                     msg='必填项验证成功',
                     payload=dict
                     )
        else:
            res = dict(code=ResponseCode.FAIL,
                       msg='参数%s未填'%str)
    else:
        res=dict(code=ResponseCode.FAIL,
                       msg='必填项未填')

    return res

import base64
import io
import random
import string
from PIL import Image, ImageFont, ImageDraw


#####################获取图片验证码#######################
class CaptchaTool(object):
    """
    生成图片验证码
    """

    def __init__(self, width=50, height=12):

        self.width = width
        self.height = height
        # 新图片对象
        self.im = Image.new('RGB', (width, height), 'white')
        # 字体
        self.font = ImageFont.load_default()
        # draw对象
        self.draw = ImageDraw.Draw(self.im)

    def draw_lines(self, num=3):
        """
        划线
        """
        for num in range(num):
            x1 = random.randint(0, self.width / 2)
            y1 = random.randint(0, self.height / 2)
            x2 = random.randint(0, self.width)
            y2 = random.randint(self.height / 2, self.height)
            self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def get_verify_code(self):
        """
        生成验证码图形
        """
        # 设置随机4位数字验证码
        code = ''.join(random.sample(string.digits, 4))
        # 绘制字符串
        for item in range(4):
            self.draw.text((6 + random.randint(-3, 3) + 10 * item, 2 + random.randint(-2, 2)),
                        text=code[item],
                        fill=(random.randint(32, 127),
                                random.randint(32, 127),
                                random.randint(32, 127))
                        , font=self.font)
        # 划线
        # self.draw_lines()
        # 重新设置图片大小
        self.im = self.im.resize((120, 32))
        # 图片转为base64字符串
        buffered = io.BytesIO()
        self.im.save(buffered, format="JPEG")
        img_str = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
        return img_str, code
def test_verify_captcha(request_body,scode):
    """
    验证图形验证码
    :return:
    """
    obj = request_body
    # 获取用户输入的验证码
    code = obj.get('code', None)
    # 获取session中的验证码
    s_code = scode
    if not all([code, s_code]):
        return {"code":403,
         "msg":'参数错误',
         "payload":{}}
    if code != s_code:
        return {"code":403,
         "msg":'验证码错误',
         "payload":{}}
    return {"code":200,
         "msg":'验证成功',
         "payload":{}}


def get_date(days,n):
    # 格式化为 年月日 形式 2019-02-25
    if n==1:
        data=(date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    else:

    # 格式化为 年月日时分秒 形式 2019-02-25 10:56:58.609985
        data=datetime.now() - timedelta(days=days)
    return data