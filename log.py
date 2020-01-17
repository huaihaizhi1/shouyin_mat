# encoding=utf-8
import logging
import datetime
import time
import smtplib
from email.mime.text import MIMEText
import logging.handlers
import os

# 日志文件的路径，FileHandler不能创建目录，这里先检查目录是否存在，不存在创建他
# 当然也可以继承之后重写FileHandler的构造函数
# month = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y%m")
# today = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y%m%d")
workdir = os.path.split(os.path.realpath(__file__))[0]
path = workdir + '/log/out.log'
LOG_FILE_PATH = path
LOG_FILE_PATH = r"C:\Users\huaihaizhi\Desktop\shouyin\log\out.log"
dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.isdir(dir):
    os.makedirs(dir)
# 写入文件的日志等级，由于是详细信息，推荐设为debug
FILE_LOG_LEVEL = "DEBUG"
# 控制台的日照等级，info和warning都可以，可以按实际要求定制
CONSOLE_LOG_LEVEL = "INFO"
# 缓存日志等级，最好设为error或者critical
MEMOEY_LOG_LEVEL = "ERROR"
# 致命错误等级
URGENT_LOG_LEVEL = "CRITICAL"

MAPPING = {"CRITICAL": 50,
           "ERROR": 40,
           "WARNING": 30,
           "INFO": 20,
           "DEBUG": 10,
           "NOTSET": 0,
           }


class logger:
    """
    logger的配置
    """

    def __init__(self, logFile, file_level, console_level):

        self.config(logFile, file_level, console_level)

    def config(self, logFile, file_level, console_level):
        # 生成root logger
        self.logger = logging.getLogger("crawler")
        self.logger.setLevel(MAPPING[file_level])
        # 生成RotatingFileHandler，设置文件大小为10M,编码为utf-8，最大文件个数为100个，如果日志文件超过100，则会覆盖最早的日志
        self.fh = logging.handlers.RotatingFileHandler(logFile, mode='a',encoding="utf-8")
        self.fh.setLevel(MAPPING[file_level])
        # 生成StreamHandler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(MAPPING[console_level])
        # 设置格式
        formatter = logging.Formatter("%(asctime)s *%(levelname)s* : %(message)s", '%Y-%m-%d %H:%M:%S')
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)

        # 把所有的handler添加到root logger中
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)


    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)

    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)

    def warning(self, msg):
        if msg is not None:
            self.logger.warning(msg)

    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)

    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)
LOG = logger(LOG_FILE_PATH, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL)


# def create_log_file():          ####生成7天日志文件#####
#     for i in range(0,7):
#         month = (datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y%m")
#         today = (datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y%m%d")
#         print(month)
#         print(today)
#         workdir=os.path.split(os.path.realpath(__file__))[0]
#         path=workdir+'/log'
#         access_file=path+'/{0}/access_{1}.log'.format(month,today)
#         error_file=path+'/{0}/error_{1}.log'.format(month,today)
#         res='pass'
#         if not os.path.isdir(path):  # 无文件夹时创建
#             try:
#                 os.makedirs(path)
#             except:
#                 res='文件夹创建失败'
#         if not os.path.isfile(access_file):  # 无文件时创建
#             try:
#                 fd = open(access_file, mode="w", encoding="utf-8")
#                 fd.close()
#             except:
#                 res='文件创建失败：{0}'.format(access_file)
#         if not os.path.isfile(error_file):  # 无文件时创建
#             try:
#                 fd = open(access_file, mode="w", encoding="utf-8")
#                 fd.close()
#             except:
#                 res='文件创建失败：{0}'.format(error_file)
#     return res
# if __name__=="__main__":
#     #测试代码
#     for i in range(50):
#         LOG.error(i)
#         LOG.debug(i)

#print(create_log_file())
