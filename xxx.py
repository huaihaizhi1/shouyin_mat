#coding=utf-8
import pymysql
import traceback

tmp = "insert into order_detail(code_id,count,goods_id,inventory_quantity,min_num,name,price_num,s_code,s_photo,seling_price,shop_id,status," \
      "threshold_remind,u_code,unit,unit_pinlei,create_time,pur_no) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"   #SQL模板字符串
l_tupple = [(i,) for i in range(100)]   #生成数据参数，list里嵌套tuple
l_tupple=[('12312344', '1', '2_10002', '123', '1', '小康不给力', '321', '123123', '', '321', '2', '0', '123', '234234', '13', '123', '2020-01-17 11:32:14', '57_1000001')]

class mymysql(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='114.67.90.231',
            port = 3306,
            user = 'webcat',
            passwd = 'webcat',
            db = 'MTDB')
        dbhost = '114.67.90.231'
        db_username = 'webcat'
        db_passwd = 'webcat'
        db_port = 3306
        db_sid = 'MTDB'

    def insert_sql(self,temp,data):
        cur = self.conn.cursor()
        try:
            cur.executemany(temp,data)
            self.conn.commit()
        except:
            self.conn.rollback()
            traceback.print_exc()
        finally:
            cur.close()

if __name__ == '__main__':
    m = mymysql()
    m.insert_sql(tmp,l_tupple)