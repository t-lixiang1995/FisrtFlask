import os

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'autodeploynb')

class DevelopmentConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/FIRST_FLASK?charset=utf8"
    # 数据库用户名:密码@host:port/数据库名?编码
    SQLALCHEMY_POOL_SIZE = 2
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = -1

    # 追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False

