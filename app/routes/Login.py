# @Time : 2019/9/3 9:41
# @Author : lixiang
# @File : Login.py
# @Software: PyCharm
from flask import Blueprint, request, jsonify

from app import auth
from app.models.user import User, Role, Resource
from flask import g
Login = Blueprint('sys', __name__)

#登录
@Login.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_json = request.get_json()
        accName = (request_json['accName'] if ('accName' in request_json) else "")
        password = (request_json['password'] if ('password' in request_json) else "")
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            user = User.query.filter(User.accName == accName).first()
            if user == None:
                api_response["code"] = 401
                api_response["message"] = "用户不存在"
                return jsonify(api_response), 401
            very = user.very_password(password)
            if very==False:
                api_response["code"] = 401
                api_response["message"] = "账号或密码不正确"
                return jsonify(api_response), 401
            elif user.status==0:
                api_response["code"] = 401
                api_response["message"] = "账号已被封禁,请联系管理员"
                return jsonify(api_response), 401
            else:
                token = bytes.decode(user.generate_auth_token(2592000))
                print(token)
                api_response['message'] = token
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] = 500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response), 500

# @Login.route('/logout', methods=['GET'])
# def logout():
#     if request.method == 'GET':
#         api_response = {
#             "code": 200,
#             "type": "",
#             "message": "请求成功"
#         }
#         try:
#             user = User.query.filter(User.id == g.user).first()
#             token = bytes.decode(user.generate_auth_token(2592000))
#             api_response['message'] = token
#             return jsonify(api_response)
#         except Exception as e:
#             #print(e)
#             api_response["code"] = 500
#             api_response["message"] = "服务器未知错误"
#             return jsonify(api_response), 500


#导航菜单
@Login.route('/menu/nav', methods=['GET'])
@auth.login_required
def nav():
    if request.method == 'GET':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            user = User.query.filter(User.accName == g.user).first()
            if user == None:
                api_response["code"] = 400
                api_response["message"] = "该账户不存在"
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
            return jsonify(response)
        except Exception as e:
            print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500