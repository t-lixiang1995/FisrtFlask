# @Time : 2019/9/3 9:41
# @Author : lixiang
# @File : Login.py
# @Software: PyCharm
import os
from datetime import datetime

from flask import Blueprint, request, jsonify,send_file
from MyLogger import Logger
from app import auth, db
from app.models.log import Last_Online
from app.models.user import User, Role, Resource
from flask import g

from common.errors import ValidationError
Login = Blueprint('sys', __name__)
IMG_DIRS = "../imgs"

#登录
@Login.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        request_json = request.get_json()
        if 'accName' not in request_json or request_json['accName'] is "":
            raise ValidationError("参数不能为空")
        accName = request_json['accName']
        if 'password' not in request_json or request_json['password'] is "":
            raise ValidationError("参数不能为空")
        password = request_json['password']
        try:
            user = User.query.filter(User.accName == accName).first()
            if user == None:
                api_response["code"] = 401
                api_response["msg"] = "用户不存在"
                return jsonify(api_response), 401
            very = user.very_password(password)
            if very==False:
                api_response["code"] = 401
                api_response["msg"] = "账号或密码不正确"
                return jsonify(api_response), 401
            elif user.status==0:
                api_response["code"] = 401
                api_response["msg"] = "账号已被封禁,请联系管理员"
                return jsonify(api_response), 401
            else:
                last_login = Last_Online.query.filter(Last_Online.accName == accName).first()
                if last_login is None:
                    new_last_login = Last_Online(accName,user.userName,datetime.now(),1)
                    db.session.add(new_last_login)
                else:
                    last_login.last_login_time = datetime.now()
                    last_login.login_count = last_login.login_count + 1
                try:
                    db.session.commit()
                except Exception as ie:
                    Logger('error.log', level='error').logger.error("[事务提交失败]accName:【%s】%s" % (accName, ie))
                    db.session.rollback()
                token = bytes.decode(user.generate_auth_token(2592000))
                api_response['expire'] = 3600
                api_response['token'] = token
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[登录异常]accName:【%s】%s" % (accName, e))
            api_response["code"] = 500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response), 500


#导航菜单
@Login.route('/menu/nav', methods=['GET'])
@auth.login_required
def nav():
    if request.method == 'GET':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            user = User.query.filter(User.accName == g.user).first()
            if user == None:
                api_response["code"] = 400
                api_response["msg"] = "该账户不存在"
                return jsonify(api_response), 400
            menuList = []
            location = []
            currrole = Role.query.filter(Role.id == user.role_id).first()
            roleToResourceS = currrole.participateResource.all()
            for roleToResource in roleToResourceS:
                currResource = Resource.query.filter(Resource.id == roleToResource.id).first()
                if currResource.type == 1:
                    menuList.append(currResource.name)
                    location.append(currResource.url)
            response = dict(menuList = menuList,location = location)
            api_response['result'] = response
            return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[获取菜单异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] =  500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response),500


#查询首页信息
@Login.route('/imgs/<string:img>', methods=['GET'])
def get_file_content(img):
    imageFile = os.path.join(IMG_DIRS,img)
    return send_file(imageFile)
