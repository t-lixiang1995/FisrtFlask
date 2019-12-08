# @Time : 2019/9/17 14:11
# @Author : lixiang
# @File : userManage.py
# @Software: PyCharm
from flask import Blueprint, request,jsonify
from app.models.user import User, Role, Resource, Enterprise
from datetime import datetime
from app import db, auth
from flask import g

from app.routes import very_permission

UserManage = Blueprint('usermanage', __name__)


#获取当前登录用户信息
@UserManage.route('/curuserInfo', methods=['GET'])
@auth.login_required
def getCurrentUserInfo():
    if request.method == 'GET':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:info").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very==False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                user = User.query.filter(User.accName == g.user).first()
                if user == None:
                    api_response["code"] = 400
                    api_response["message"] = "该账户不存在"
                    return jsonify(api_response), 400
                response = dict(accName=user.accName, userID=user.userID, accType=user.role_id, userName=user.userName,
                                accAttr=user.accAttr, etpName=user.etpName, userDP=user.userDP, userMail=user.userMail,
                                userPhone=user.userPhone, userTel=user.userTel)
                return jsonify(response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#删除指定用户
@UserManage.route('/delete/<string:accName>', methods=['GET'])
@auth.login_required
def deleteUserInfo(accName):
    if request.method == 'GET':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:delete").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very==False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                user = User.query.filter(User.accName == accName).first()
                if user == None:
                    api_response["code"] = 400
                    api_response["message"] = "删除失败，账户不存在"
                    return jsonify(api_response), 400
                db.session.delete(user)
                db.session.commit()
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#获取指定用户信息
@UserManage.route('/info/<string:accName>', methods=['GET'])
@auth.login_required
def getUserInfo(accName):
    if request.method == 'GET':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:info").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very==False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                user = User.query.filter(User.accName == accName).first()
                if user == None:
                    api_response["code"] = 400
                    api_response["message"] = "该账户不存在"
                    return jsonify(api_response), 400
                response = dict(accName=user.accName, userID=user.userID, accType=user.role_id, userName=user.userName,
                                accAttr=user.accAttr, etpName=user.etpName, userDP=user.userDP, userMail=user.userMail,
                                userPhone=user.userPhone, userTel=user.userTel)
                return jsonify(response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#获取用户信息列表
@UserManage.route('/list', methods=['GET'])
@auth.login_required
def getUserList():
    if request.method == 'GET':
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        accName = request.args.get("accName", "")
        etpCode = request.args.get("etpCode", "")
        etpName = request.args.get("etpName", "")
        accType = int(request.args.get("accType", 0))
        filters = {User.status == 1}
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:list").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                userList = []
                if accName is not "":
                    filters.add(User.accName.like("%"+accName+"%"))
                if etpCode is not "":
                    filters.add(User.accAttr == etpCode)
                if etpName is not "":
                    filters.add(User.etpName.like("%" + etpName + "%"))
                if accType is not 0:
                    filters.add(User.role_id == accType)
                userlist = User.query.filter(*filters).limit(limit).offset((page - 1) * limit).all()
                sumList = User.query.filter(*filters).all()
                for user in userlist:
                    userList.append(dict(accName=user.accName, userName=user.userName, accType=user.role_id,
                                         userDP=user.userDP, etpName=user.etpName, createTime=user.create_date))
                result = dict(sumcount=len(sumList), detailcount=len(userlist), data=userList)
                return jsonify(result)
        except Exception as e:
            print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#修改用户所属角色
@UserManage.route('/update', methods=['POST'])
@auth.login_required
def editUserPermission():
    if request.method == 'POST':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:update").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                request_json = request.get_json()
                accName = (request_json['accName'] if ('accName' in request_json) else "")
                accType = (request_json['accType'] if ('accType' in request_json) else "")
                user = User.query.filter(User.accName == accName).first()
                if user == None:
                    api_response["code"] = 400
                    api_response["message"] = "所修改账户不存在"
                    return jsonify(api_response), 400
                user.role_id = accType
                db.session.commit()
                return jsonify(api_response)
        except Exception as e:
            print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#新增用户
@UserManage.route('/save', methods=['POST'])
@auth.login_required
def createUser():
    if request.method == 'POST':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:save").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                request_json = request.get_json()
                accName = (request_json['accName'] if ('accName' in request_json) else "")
                accType = (request_json['accType'] if ('accType' in request_json) else "")
                userID = (request_json['userID'] if ('userID' in request_json) else "")
                userName = (request_json['userName'] if ('userName' in request_json) else "")
                accAttr = (request_json['accAttr'] if ('accAttr' in request_json) else "")
                etpName = (request_json['etpName'] if ('etpName' in request_json) else "")
                userDP = (request_json['userDP'] if ('userDP' in request_json) else "")
                userMail = (request_json['userMail'] if ('userMail' in request_json) else "")
                userPhone = (request_json['userPhone'] if ('userPhone' in request_json) else "")
                userTel = (request_json['userTel'] if ('userTel' in request_json) else "")
                password = (request_json['password'] if ('password' in request_json) else "")
                status = (request_json['status'] if ('status' in request_json) else 1)
                create_user_id = g.user
                create_date = (request_json['create_date'] if ('create_date' in request_json) else datetime.now())
                remarks = (request_json['remarks'] if ('remarks' in request_json) else "")
                if accName == "" or password == "" or accType == "" or userID == "" or userName == "" or accAttr == "" \
                        or etpName == "" or userDP == "" or userMail == "" or userPhone == "" or userTel == "":
                    api_response["code"] = 400
                    api_response["message"] = "请求参数错误"
                    return jsonify(api_response), 400
                newUser = User(accName, userID, userName, userMail, userPhone, userTel, password, status,
                               accType, accAttr, etpName, userDP, create_date, create_user_id, remarks)
                newUser.hash_pwd(password)
                db.session.add(newUser)
                db.session.commit()
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#修改用户密码
@UserManage.route('/update/pwd/<string:oldPassword>/<string:password>/<string:reppassword>', methods=['GET'])
@auth.login_required
def editUserPassword(oldPassword,password,reppassword):
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
            elif user.very_password(oldPassword)==False:
                api_response["code"] = 400
                api_response["message"] = "原始密码输入有误"
                return jsonify(api_response)
            elif password != reppassword:
                api_response["code"] = 400
                api_response["message"] = "两次密码不一致"
                return jsonify(api_response)
            else:
                user.hash_pwd(password)
                db.session.commit()
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


#修改用户信息
@UserManage.route('/sysUser/update', methods=['POST'])
@auth.login_required
def editUser():
    if request.method == 'POST':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:usermanage:update").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["message"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["message"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                request_json = request.get_json()
                accName = (request_json['accName'] if ('accName' in request_json) else "")
                userID = (request_json['userID'] if ('userID' in request_json) else "")
                userName = (request_json['userName'] if ('userName' in request_json) else "")
                accAttr = (request_json['accAttr'] if ('accAttr' in request_json) else "")
                etpName = (request_json['etpName'] if ('etpName' in request_json) else "")
                userDP = (request_json['userDP'] if ('userDP' in request_json) else "")
                userMail = (request_json['userMail'] if ('userMail' in request_json) else "")
                userPhone = (request_json['userPhone'] if ('userPhone' in request_json) else "")
                userTel = (request_json['userTel'] if ('userTel' in request_json) else "")
                if accName == "" or userID == "" or userName == "" or accAttr == "" \
                        or etpName == "" or userDP == "" or userMail == "" or userPhone == "" or userTel == "":
                    api_response["code"] = 400
                    api_response["message"] = "请求参数错误"
                    return jsonify(api_response), 400
                user = User.query.filter(User.accName == accName,User.userID == userID,User.userName == userName,
                                         User.accAttr == accAttr,User.etpName == etpName,User.userDP == userDP).first()
                if user == None:
                    api_response["code"] = 400
                    api_response["message"] = "该账户不存在"
                    return jsonify(api_response), 400
                if ('accType' in request_json):
                    user.role_id = request_json['accType']
                user.userMail = userMail
                user.userPhone = userPhone
                user.userTel = userTel
                if ('password' in request_json):
                    user.hash_pwd(request_json['password'])
                if ('status' in request_json):
                    user.status = request_json['status']
                if ('remarks' in request_json):
                    user.remarks = request_json['remarks']
                db.session.commit()
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500