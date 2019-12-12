
import pymysql
import hashlib
from config import db_username,db_passwd,db_port,db_sid,dbhost
def my_db(sql):   #连接mysql
    coon = pymysql.connect(
        host=dbhost, user=db_username, passwd=db_passwd,
        port=db_port, db=db_sid, charset='utf8')
    cur = coon.cursor(cursor=pymysql.cursors.DictCursor) #建立游标
    if sql.strip()[:6].upper()=='SELECT':
        cur.execute(sql)  # 执行sql
        res =  cur.fetchall()
    else:
        try:
            cur.execute(sql)  # 执行sql
            coon.commit()
            res = 'ok'
        except:
            coon.rollback()
            res='false'
    cur.close()
    coon.close()
    return res

def my_md5(s,salt='xxkdjkd'):      #加盐，盐的默认值是空
    s=s+salt
    news=str(s).encode()    #先变成bytes类型才能加密
    m=hashlib.md5(news)     #创建md5对象
    return m.hexdigest()    #获取加密后的字符串