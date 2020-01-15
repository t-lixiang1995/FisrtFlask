# @Time : 2020/1/15 16:33 
# @Author : lixiang
# @File : log.py 
# @Software: PyCharm
from datetime import datetime

from app import db


class Last_Online(db.Model):
    __tablename__ = 'sys_user_last_online'
    id = db.Column(db.INT, nullable=False, primary_key=True, autoincrement=True)
    accName = db.Column(db.String(50))
    userName = db.Column(db.String(50))
    last_login_time = db.Column(db.DATETIME, default=datetime.now(), nullable=False, comment="最后登录时间")
    login_count = db.Column(db.INT, comment="登录次数")
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    def __init__(self, accName="", userName="", last_login_time="", login_count=""):
        self.accName = accName
        self.userName = userName
        self.last_login_time = last_login_time
        self.login_count = login_count