# @Time : 2019/9/3 15:09
# @Author : lixiang
# @File : user.py
# @Software: PyCharm
from app import db
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
import os
import  time


Role_To_Resource = db.Table('roleToResource',db.Column('role_id',db.BIGINT,db.ForeignKey('sys_role.id'),primary_key=True) ,db.Column('resource_id',db.BIGINT,db.ForeignKey('sys_resource.id'),primary_key=True))
class User(db.Model):
    __tablename__ = 'sys_user'
    accName = db.Column(db.String(50), primary_key=True, nullable=False)           #登录账号
    userID = db.Column(db.String(20), nullable=False)                              #AD账号
    userName = db.Column(db.String(50), nullable=False)                            #姓名
    userMail = db.Column(db.String(50), nullable=False)                            #邮箱
    userPhone = db.Column(db.String(20), nullable=False)                           #手机号
    userTel = db.Column(db.String(20), nullable=False)                             #电话
    password = db.Column(db.String(128), nullable=False, default="")               #登录密码
    status = db.Column(db.INT)                                                     #0 已禁用   1 使用中
    role_id = db.Column(db.BIGINT, nullable=False)                                 #1:超级管理员 2:企业管理员 3：普通用户
    accAttr = db.Column(db.String(20), nullable=False)                             #企业编码
    etpName = db.Column(db.String(50), nullable=False)                             #企业名称
    userDP = db.Column(db.String(50), nullable=False)                              #部门
    create_date = db.Column(db.DATETIME, default=datetime.now())                   #创建日期
    create_user_id = db.Column(db.String(50))                                      #创建人
    remarks = db.Column(db.String(100))                                            #备注（预留字段）
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __init__(self, accName="", userID="", userName="", userMail="", userPhone="", userTel="", password="",
                 status="", role_id="",accAttr="", etpName="", userDP="", create_date="", create_user_id="",remarks=""):
        self.accName = accName
        self.userID = userID
        self.userName = userName
        self.userMail = userMail
        self.userPhone = userPhone
        self.userTel = userTel
        self.password = password
        self.status = status
        self.role_id = role_id
        self.accAttr = accAttr
        self.etpName = etpName
        self.userDP = userDP
        self.create_date = create_date
        self.create_user_id = create_user_id
        self.remarks = remarks

    def hash_pwd(self, password):
        self.password = pwd_context.encrypt(password)

    def very_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(os.getenv('SECRET_KEY', 'autodeploynb'), expires_in=expiration)
        print(os.getenv('SECRET_KEY', 'autodeploynb'))
        expireDate = int(time.time()) + expiration
        return s.dumps({"accName": self.accName,"userName": self.userName, "role": self.role_id,"accAttr": self.accAttr,"userDP": self.userDP,"expireDate": expireDate})


class Role(db.Model):
    __tablename__ = 'sys_role'
    id = db.Column(db.BIGINT, primary_key=True,autoincrement=True, nullable=False)              #角色ID
    name = db.Column(db.String(100))                                                            #角色名称
    role = db.Column(db.String(100))                                                            #角色编码
    description = db.Column(db.String(200))                                                     #角色描述
    is_show = db.Column(db.INT)                                                                 # 0：已弃用 1：使用中
    create_date = db.Column(db.DATETIME, default=datetime.now(), nullable=False)                #创建日期
    participateResource = db.relationship('Resource',secondary = Role_To_Resource ,back_populates = 'participants',lazy = 'dynamic')
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __init__(self, description="", is_show=1):
        self.description = description
        self.is_show = is_show


class Resource(db.Model):
    __tablename__ = 'sys_resource'
    id = db.Column(db.BIGINT, primary_key=True,autoincrement=True)         #权限ID
    name = db.Column(db.String(50))                                        #权限名称
    url = db.Column(db.String(200))                                        #跳转路径
    perms = db.Column(db.String(500))                                      #权限编码
    parent_id = db.Column(db.BIGINT)                                       #父级权限ID
    type = db.Column(db.INT)                                               #权限类型 1：菜单权限 2：功能权限
    icon = db.Column(db.String(50))                                        #图标
    weight = db.Column(db.INT)                                             #权重
    is_show = db.Column(db.INT)                                            # 0：已弃用  1：使用中
    participants = db.relationship('Role', secondary=Role_To_Resource, back_populates='participateResource')
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __init__(self, weight=0, is_show=1):
        self.weight = weight
        self.is_show = is_show


class Enterprise(db.Model):
    __tablename__ = 'ads_enterpriselist'
    etpCode = db.Column(db.String(60), primary_key=True, nullable=False)                     #企业编号
    etpName = db.Column(db.String(20), nullable=False)                                       #企业名称
    LDAPCode = db.Column(db.String(20), nullable=False)                                      #LDAP编码
    accType = db.Column(db.BIGINT)                                                           #账号类型
    dhcpServerIP = db.Column(db.String(20))                                                  #DHCP服务器IP
    TFTPServerIP = db.Column(db.String(20))                                                  #TFTP服务器IP
    FTPServerIP = db.Column(db.String(20))                                                   #FTP服务器IP
    isDelete = db.Column(db.BIGINT)                                                          # 0:已弃用 1：使用中
    createAdmin = db.Column(db.String(50))                                                   #创建管理员
    createTime = db.Column(db.DATETIME, default=datetime.now(), nullable=False)              #创建时间
    updateTime = db.Column(db.DATETIME)                                                      #更新时间
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __init__(self, etpCode="", etpName="", LDAPCode="", accType="", dhcpServerIP="", TFTPServerIP="",
                 FTPServerIP="", isDelete="", createAdmin="", createTime=""):
        self.etpCode = etpCode
        self.etpName = etpName
        self.LDAPCode = LDAPCode
        self.accType = accType
        self.dhcpServerIP = dhcpServerIP
        self.TFTPServerIP = TFTPServerIP
        self.FTPServerIP = FTPServerIP
        self.isDelete = isDelete
        self.createAdmin = createAdmin
        self.createTime = createTime


class Server(db.Model):
    __tablename__ = 'ads_etpServerlist'
    etpCode = db.Column(db.String(60), db.ForeignKey('ads_enterpriselist.etpCode'), primary_key=True, nullable=False)   #企业编码
    serverType = db.Column(db.INT,primary_key=True, nullable=False)                                                     #1:DHCP 服务器 2:TFTP服务器 3:FTP服务器
    serverIP = db.Column(db.String(20))                                                                                 #服务器IP
    serverUsername = db.Column(db.String(20))                                                                           #服务器用户名
    serverPasswd = db.Column(db.String(50))                                                                             #服务器密码
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __init__(self, etpCode="", serverType="", serverIP="", serverUsername="", serverPasswd=""):
        self.etpCode = etpCode
        self.serverType = serverType
        self.serverIP = serverIP
        self.serverUsername = serverUsername
        self.serverPasswd = serverPasswd
