# @Time : 2019/9/24 11:26
# @Author : lixiang
# @File : enterprise.py
# @Software: PyCharm
from flask import Blueprint, request,jsonify
from app.models.user import Enterprise, Server, User, Role, Resource
from datetime import datetime
from app import db, auth
from flask import g

from app.routes import very_permission

EnterpriseManage = Blueprint('enterprise', __name__)


@EnterpriseManage.route('/save', methods=['POST'])
@auth.login_required
def createEnterprise():
    if request.method == 'POST':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:save").first()
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
                etpCode = (request_json['etpCode'] if ('etpCode' in request_json) else "")
                etpName = (request_json['etpName'] if ('etpName' in request_json) else "")
                LDAPCode = (request_json['LDAPCode'] if ('LDAPCode' in request_json) else "")
                accType = (request_json['accType'] if ('accType' in request_json) else 0)
                dhcpServerIP = (request_json['dhcpServerIP'] if ('dhcpServerIP' in request_json) else "")
                TFTPServerIP = (request_json['TFTPServerIP'] if ('TFTPServerIP' in request_json) else "")
                FTPServerIP = (request_json['FTPServerIP'] if ('FTPServerIP' in request_json) else "")
                isDelete = (request_json['isDelete'] if ('isDelete' in request_json) else 1)
                serverInfolist = (request_json['serverInfolist'] if ('serverInfolist' in request_json) else "")
                createAdmin = g.user
                createTime = (request_json['createTime'] if ('createTime' in request_json) else datetime.now())
                if etpCode == "" or etpName == "" or LDAPCode == "" or serverInfolist == "":
                    api_response["code"] = 400
                    api_response["message"] = "请求参数错误"
                    return jsonify(api_response), 400
                newenterprise = Enterprise(etpCode, etpName, LDAPCode, accType , dhcpServerIP,
                                           TFTPServerIP, FTPServerIP, isDelete, createAdmin, createTime)
                db.session.add(newenterprise)
                db.session.commit()
                for serverinfo in serverInfolist:
                    serverType = (serverinfo['serverType'] if ('serverType' in serverinfo) else "")
                    serverIP = (serverinfo['serverIP'] if ('serverIP' in serverinfo) else "")
                    serverUsername = (serverinfo['serverUsername'] if ('serverUsername' in serverinfo) else "")
                    serverPasswd = (serverinfo['serverPasswd'] if ('serverPasswd' in serverinfo) else "")
                    if serverType == "":
                        api_response["code"] = 400
                        api_response["message"] = "请求参数错误"
                        return jsonify(api_response), 400
                    newServer = Server(etpCode, serverType, serverIP, serverUsername, serverPasswd)
                    db.session.add(newServer)
                    db.session.commit()
                api_response["message"] = etpCode
                return jsonify(api_response)
        except Exception as e:
            print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500


@EnterpriseManage.route('/delete/<string:etpCode>', methods=['GET'])
@auth.login_required
def deleteEnterprise(etpCode):
    if request.method == 'GET':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:delete").first()
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
                enterprise = Enterprise.query.filter(Enterprise.etpCode == etpCode).first()
                server = Server.query.filter(Server.etpCode == etpCode).first()
                if enterprise == None:
                    api_response["code"] = 400
                    api_response["message"] = "该组织机构不存在"
                    return jsonify(api_response), 400
                if server != None:
                    Server.query.filter(Server.etpCode == etpCode).delete()
                    db.session.commit()
                db.session.delete(enterprise)
                db.session.commit()
                api_response["message"] = etpCode
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] = 500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response), 500


@EnterpriseManage.route('/update', methods=['POST'])
@auth.login_required
def editEnterprise():
    if request.method == 'POST':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:update").first()
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
                etpCode = (request_json['etpCode'] if ('etpCode' in request_json) else "")
                enterprise = Enterprise.query.filter(Enterprise.etpCode == etpCode).first()
                if enterprise == None:
                    api_response["code"] = 400
                    api_response["message"] = "该组织机构不存在"
                    return jsonify(api_response), 400
                updateTime = (request_json['updateTime'] if ('updateTime' in request_json) else datetime.now())
                enterprise.updateTime = updateTime
                if ('accType' in request_json):
                    enterprise.accType = request_json['accType']
                if ('dhcpServerIP' in request_json):
                    enterprise.dhcpServerIP = request_json['dhcpServerIP']
                if ('TFTPServerIP' in request_json):
                    enterprise.TFTPServerIP = request_json['TFTPServerIP']
                if ('FTPServerIP' in request_json):
                    enterprise.FTPServerIP = request_json['FTPServerIP']
                if ('isDelete' in request_json):
                    enterprise.isDelete = request_json['isDelete']
                if ('serverInfolist' in request_json):
                    serverInfoList = request_json['serverInfolist']
                    for server in serverInfoList:
                        serverType = (server['serverType'] if ('serverType' in server) else "")
                        serverInfo = Server.query.filter(Server.etpCode == etpCode,
                                                         Server.serverType == serverType).first()
                        if serverInfo==None:
                            serverIP = (server['serverIP'] if ('serverIP' in server) else "")
                            serverUsername = (server['serverUsername'] if ('serverUsername' in server) else "")
                            serverPasswd = (server['serverPasswd'] if ('serverPasswd' in server) else "")
                            newServer = Server(etpCode, serverType, serverIP, serverUsername, serverPasswd)
                            db.session.add(newServer)
                            db.session.commit()
                        else:
                            if ('serverIP' in server):
                                serverInfo.serverIP = server['serverIP']
                            if ('serverUsername' in server):
                                serverInfo.serverUsername = server['serverUsername']
                            if ('serverPasswd' in server):
                                serverInfo.serverPasswd = server['serverPasswd']
                            db.session.commit()
                db.session.commit()
                api_response["message"] = etpCode
                return jsonify(api_response)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response)

@EnterpriseManage.route('/info/<string:etpCode>', methods=['GET'])
@auth.login_required
def getEnterprise(etpCode):
    if request.method == 'GET':
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:list").first()
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
                enterprise = Enterprise.query.filter(Enterprise.etpCode == etpCode).first()
                serverList = Server.query.filter(Server.etpCode == etpCode).all()
                if enterprise == None:
                    api_response["code"] = 400
                    api_response["message"] = "该组织机构不存在"
                    return jsonify(api_response), 400
                else:
                    serverinfoList = []
                    if serverList:
                        for server in serverList:
                            serverinfoList.append(dict(etpCode=etpCode, serverType=server.serverType, serverIP=server.serverIP,
                                              serverUsername=server.serverUsername, serverPasswd=server.serverPasswd))
                    response = dict(etpCode=enterprise.etpCode, etpName=enterprise.etpName, LDAPCode=enterprise.LDAPCode, accType=enterprise.accType,
                             dhcpServerIP=enterprise.dhcpServerIP, TFTPServerIP=enterprise.TFTPServerIP, FTPServerIP=enterprise.FTPServerIP,
                             createAdmin=enterprise.createAdmin, createTime=enterprise.createTime, updateTime=enterprise.updateTime, serverInfolist=serverinfoList)
                    return jsonify(response)
        except Exception as e:
            print(e)
            api_response["code"] = 500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response), 500

@EnterpriseManage.route('/list', methods=['GET'])
@auth.login_required
def getEnterpriseList():
    if request.method == 'GET':
        page = int(request.args.get("page",1))
        limit = int(request.args.get("limit",10))
        etpCode = request.args.get("etpCode", "")
        etpName = request.args.get("etpName", "")
        filters = {Enterprise.isDelete == 1}
        api_response = {
            "code": 200,
            "type": "",
            "message": "请求成功"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:list").first()
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
                enterpriselist = []
                if etpCode is not "":
                    filters.add(Enterprise.etpCode == etpCode)
                if etpName is not "":
                    filters.add(Enterprise.etpName.like("%" + etpName + "%"))
                enterpriseList = Enterprise.query.filter(*filters).limit(limit).offset((page - 1) * limit).all()
                sumList = Enterprise.query.filter(*filters).all()
                for enterprise in enterpriseList:
                    enterpriselist.append(
                        dict(etpCode=enterprise.etpCode, etpName=enterprise.etpName, LDAPCode=enterprise.LDAPCode, accType=enterprise.accType,
                             dhcpServerIP=enterprise.dhcpServerIP, TFTPServerIP=enterprise.TFTPServerIP, FTPServerIP=enterprise.FTPServerIP,
                             createAdmin=enterprise.createAdmin, createTime=enterprise.createTime, updateTime=enterprise.updateTime))
                result = dict(sumcount=len(sumList), detailcount=len(enterpriseList), data=enterpriselist)
                return jsonify(result)
        except Exception as e:
            #print(e)
            api_response["code"] =  500
            api_response["message"] = "服务器未知错误"
            return jsonify(api_response),500