import time

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from .models import *
from flask import jsonify,g
from common import sqlhelper
from flask_httpauth import HTTPTokenAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_cors import *
from common.tool import JSONEncoder
db = SQLAlchemy()
dbhelper=None
auth = HTTPTokenAuth(scheme='Bearer')
#创建app
def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 设置跨域


    @auth.verify_token
    def verify_token(token):
        g.user = None
        s=Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            print('SignatureExpired')
            return False
        except BadSignature:
            print('BadSignature')
            return False
        if 'expireDate' in data:
            if data['expireDate'] < int(time.time()):
                print("登陆信息已失效！")
                return False
            elif 'accName' in data:
                g.user = data['accName']
                return True
        return False

    @auth.error_handler
    def unauthorized():
        return jsonify({
            "code": 401,
            "type": "",
            "message": "用户认证失败"
        }), 401
    app.json_encoder = JSONEncoder
    app.debug = True
    app.secret_key = 'sdiusdfsdf'#自定义的session秘钥
    # 设置配置文件
    app.config.from_object('settings.DevelopmentConfig')
    global dbhelper
    dbhelper = sqlhelper.SQLHelper()
    db.init_app(app)
    # 注册蓝图
    from .routes.enterprise import EnterpriseManage
    app.register_blueprint(EnterpriseManage, url_prefix='/modules/enterprise')
    from .routes.Login import Login
    app.register_blueprint(Login, url_prefix='/sys')
    from .routes.userManage import UserManage
    app.register_blueprint(UserManage, url_prefix='/modules/usermanage')
    # 注册组件
    # Session(app)
    #Auth(app)

    # 2. 注册 Flask-SQLAlchemy
    # 这个对象在其他地方想要使用
    # SQLAlchemy(app)



    return app