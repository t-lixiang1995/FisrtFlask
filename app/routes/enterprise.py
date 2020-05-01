# @Time : 2019/9/24 11:26
# @Author : lixiang
# @File : enterprise.py
# @Software: PyCharm
import os
import time

import paramiko
from flask import Blueprint, request, jsonify, Response

from MyLogger import Logger
from app.models.user import Enterprise, Server,Resource
from datetime import datetime
from app import db, auth
from flask import g

from app.routes import very_permission
from common.errors import ValidationError
EnterpriseManage = Blueprint('enterprise', __name__)
UPLOADFILES_DIRS = "./files/enterprise"


@EnterpriseManage.route('/save', methods=['POST'])
@auth.login_required
def createEnterprise():
    if request.method == 'POST':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:save").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                request_json = request.get_json()
                # if 'etpCode' not in request_json or request_json['etpCode'] is "":
                #     raise ValidationError("参数不能为空")
                # etpCode = request_json['etpCode']
                if 'etpName' not in request_json or request_json['etpName'] is "":
                    raise ValidationError("参数不能为空")
                etpName = request_json['etpName']
                if 'LDAPCode' not in request_json or request_json['LDAPCode'] is "":
                    raise ValidationError("参数不能为空")
                LDAPCode = request_json['LDAPCode']
                etpCode = LDAPCode + "_" + str(int(time.time() * 10))
                if 'serverInfolist' not in request_json or request_json['serverInfolist'] is "":
                    raise ValidationError("参数不能为空")
                serverInfolist = request_json['serverInfolist']
                dhcpServerIP = (request_json['dhcpServerIP'] if ('dhcpServerIP' in request_json) else "")
                TFTPServerIP = (request_json['TFTPServerIP'] if ('TFTPServerIP' in request_json) else "")
                FTPServerIP = (request_json['FTPServerIP'] if ('FTPServerIP' in request_json) else "")
                createAdmin = g.user
                createTime = (request_json['createTime'] if ('createTime' in request_json) else datetime.now())
                newenterprise = Enterprise(etpCode, etpName, LDAPCode, dhcpServerIP, TFTPServerIP, FTPServerIP, createAdmin, createTime)
                db.session.add(newenterprise)
                for serverinfo in serverInfolist:
                    if 'serverType' not in serverinfo or serverinfo['serverType'] is "":
                        raise ValidationError("参数不能为空")
                    serverType = serverinfo['serverType']
                    serverIP = (serverinfo['serverIP'] if ('serverIP' in serverinfo) else "")
                    serverUsername = (serverinfo['serverUsername'] if ('serverUsername' in serverinfo) else "")
                    serverPasswd = (serverinfo['serverPasswd'] if ('serverPasswd' in serverinfo) else "")
                    newServer = Server(etpCode, serverType, serverIP, serverUsername, serverPasswd)
                    db.session.add(newServer)
                try:
                    db.session.commit()
                except Exception as ie:
                    Logger('error.log', level='error').logger.error("[事务提交失败]accName:【%s】%s" % (g.user, ie))
                    db.session.rollback()
                api_response["result"] = etpCode
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[添加企业异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] =  500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response),500


@EnterpriseManage.route('/delete/<string:etpCode>', methods=['GET'])
@auth.login_required
def deleteEnterprise(etpCode):
    if request.method == 'GET':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:delete").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                enterprise = Enterprise.query.filter(Enterprise.etpCode == etpCode).first()
                server = Server.query.filter(Server.etpCode == etpCode).first()
                if enterprise == None:
                    api_response["code"] = 400
                    api_response["msg"] = "该组织机构不存在"
                    return jsonify(api_response), 400
                if server != None:
                    Server.query.filter(Server.etpCode == etpCode).delete()
                db.session.delete(enterprise)
                try:
                    db.session.commit()
                except Exception as ie:
                    Logger('error.log', level='error').logger.error("[事务提交失败]accName:【%s】%s" % (g.user, ie))
                    db.session.rollback()
                api_response["result"] = etpCode
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[删除企业异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] = 500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response), 500


@EnterpriseManage.route('/update', methods=['POST'])
@auth.login_required
def editEnterprise():
    if request.method == 'POST':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:update").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                request_json = request.get_json()
                if 'etpCode' not in request_json or request_json['etpCode'] is "":
                    raise ValidationError("参数不能为空")
                etpCode = request_json['etpCode']
                enterprise = Enterprise.query.filter(Enterprise.etpCode == etpCode).first()
                if enterprise == None:
                    api_response["code"] = 400
                    api_response["msg"] = "该组织机构不存在"
                    return jsonify(api_response), 400
                updateTime = (request_json['updateTime'] if ('updateTime' in request_json) else datetime.now())
                enterprise.updateTime = updateTime
                if ('dhcpServerIP' in request_json):
                    enterprise.dhcpServerIP = request_json['dhcpServerIP']
                if ('TFTPServerIP' in request_json):
                    enterprise.TFTPServerIP = request_json['TFTPServerIP']
                if ('FTPServerIP' in request_json):
                    enterprise.FTPServerIP = request_json['FTPServerIP']
                if ('serverInfolist' in request_json):
                    serverInfoList = request_json['serverInfolist']
                    for server in serverInfoList:
                        serverType = (server['serverType'] if ('serverType' in server) else "")
                        serverInfo = Server.query.filter(Server.etpCode == etpCode,Server.serverType == serverType).first()
                        if serverInfo==None:
                            api_response["code"] = 400
                            api_response["msg"] = "该服务器信息不存在"
                            return jsonify(api_response), 400
                        if ('serverIP' in server):
                            serverInfo.serverIP = server['serverIP']
                        if ('serverUsername' in server):
                            serverInfo.serverUsername = server['serverUsername']
                        if ('serverPasswd' in server):
                            serverInfo.serverPasswd = server['serverPasswd']
                try:
                    db.session.commit()
                except Exception as ie:
                    Logger('error.log', level='error').logger.error("[事务提交失败]accName:【%s】%s" % (g.user, ie))
                    db.session.rollback()
                api_response["result"] = etpCode
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[修改企业信息异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] =  500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response)

# 批量删除企业
@EnterpriseManage.route('/deleteBatch', methods=['POST'])
@auth.login_required
def deleteBatch():
    if request.method == 'POST':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:delete").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                request_json = request.get_json()
                etpCodeList = (request_json['etpCodeList'] if ('etpCodeList' in request_json) else "")
                for etpCode in etpCodeList:
                    enter = Enterprise.query.filter(Enterprise.etpCode==etpCode).first()
                    server = Server.query.filter(Server.etpCode == etpCode).first()
                    if enter == None:
                        api_response["code"] = 400
                        api_response["msg"] = "该组织机构不存在"
                        return jsonify(api_response), 400
                    if server != None:
                        Server.query.filter(Server.etpCode == etpCode).delete()
                    db.session.delete(enter)
                try:
                    db.session.commit()
                except Exception as ie:
                    Logger('error.log', level='error').logger.error("[事务提交失败]accName:【%s】%s" % (g.user, ie))
                    db.session.rollback()
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[批量删除企业异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] =  500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response),500

@EnterpriseManage.route('/info/<string:etpCode>', methods=['GET'])
@auth.login_required
def getEnterprise(etpCode):
    if request.method == 'GET':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:list").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                enterprise = Enterprise.query.filter(Enterprise.etpCode == etpCode).first()
                serverList = Server.query.filter(Server.etpCode == etpCode).all()
                if enterprise == None:
                    api_response["code"] = 400
                    api_response["msg"] = "该组织机构不存在"
                    return jsonify(api_response), 400
                else:
                    data = []
                    serverinfoList = []
                    if serverList:
                        for server in serverList:
                            serverinfoList.append(dict(etpCode=etpCode, serverType=server.serverType, serverIP=server.serverIP,
                                              serverUsername=server.serverUsername, serverPasswd=server.serverPasswd))
                    data.append(dict(etpCode=enterprise.etpCode, etpName=enterprise.etpName, LDAPCode=enterprise.LDAPCode,
                             dhcpServerIP=enterprise.dhcpServerIP, TFTPServerIP=enterprise.TFTPServerIP, FTPServerIP=enterprise.FTPServerIP,
                             createAdmin=enterprise.createAdmin, createTime=enterprise.createTime, updateTime=enterprise.updateTime, serverInfolist=serverinfoList))
                    response = dict(list=data)
                    api_response['result'] = response
                    return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[查询企业信息异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] = 500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response), 500

@EnterpriseManage.route('/list', methods=['GET'])
@auth.login_required
def getEnterpriseList():
    if request.method == 'GET':
        page = int(request.args.get("page",1))
        limit = int(request.args.get("limit",10))
        etpCode = request.args.get("etpCode", "")
        etpName = request.args.get("etpName", "")
        filters = {1 == 1}
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:list").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
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
                        dict(etpCode=enterprise.etpCode, etpName=enterprise.etpName, LDAPCode=enterprise.LDAPCode,
                             dhcpServerIP=enterprise.dhcpServerIP, TFTPServerIP=enterprise.TFTPServerIP, FTPServerIP=enterprise.FTPServerIP,
                             createAdmin=enterprise.createAdmin, createTime=enterprise.createTime, updateTime=enterprise.updateTime))
                result = dict(sumcount=len(sumList), detailcount=len(enterpriseList), list=enterpriselist)
                api_response['result'] = result
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[查询企业列表异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] =  500
            api_response["msg"] = "服务器未知错误"
            return jsonify(api_response),500


#下载文件
@EnterpriseManage.route('/downLoad/<string:fileName>', methods=['GET'])
@auth.login_required
def downLoad(fileName):
    if request.method == 'GET':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:list").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                files = os.path.join(UPLOADFILES_DIRS, fileName)
                if os.path.exists(files):
                    # 流式读取
                    def send_file():
                        store_path = files
                        with open(store_path, 'rb') as targetfile:
                            while 1:
                                data = targetfile.read(20 * 1024 * 1024)  # 每次读取20M
                                if not data:
                                    break
                                yield data
                    response = Response(send_file(), content_type='application/octet-stream')
                    response.headers["Content-disposition"] = 'attachment; filename=%s' % fileName  # 如果不加上这行代码，导致下图的问题
                    return response
                api_response["code"] = 400
                api_response["msg"] = "文件不存在！"
                return jsonify(api_response)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[下载文件异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] = 400
            api_response["msg"] = "系统异常"
            return jsonify(api_response)


#上传图片临时保存文件
@EnterpriseManage.route('/upLoad', methods=['POST'])
@auth.login_required
def upload():
    if request.method == 'POST':
        api_response = {
            "code": 0,
            "msg": "success"
        }
        try:
            currResource = Resource.query.filter(Resource.perms == "modules:enterprise:save").first()
            if currResource==None:
                api_response["code"] = 401
                api_response["msg"] = "当前操作权限实体不存在"
                return jsonify(api_response), 401
            very = very_permission(currResource.id)
            if very == False:
                api_response["code"] = 401
                api_response["msg"] = "该账户无操作权限"
                return jsonify(api_response), 401
            else:
                files = request.files.getlist("excelFile")
                for file in files:
                    filename = file.filename
                    if not os.path.exists(UPLOADFILES_DIRS):
                        os.makedirs(UPLOADFILES_DIRS)
                    newFilePath = os.path.join(UPLOADFILES_DIRS, filename)
                    file.save(newFilePath)
        except Exception as e:
            Logger('error.log', level='error').logger.error("[上传文件异常]accName:【%s】%s" % (g.user, e))
            api_response["code"] = 400
            api_response["msg"] = "系统异常"
            return jsonify(api_response)
        api_response["result"] = filename
        return jsonify(api_response)


#通过SSH连接服务器执行命令脚本
def getNetByIPAndMask(ip,mask):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname='192.168.141.130', port=22, username='root', password='root')
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command('cd /home/smcc/smcc-crst/SMCC_NEW/bin;./ipResponse ' + ip + ' ' + mask,get_pty=True)
    # 获取命令结果
    result = stdout.read()
    # 关闭连接
    ssh.close()
    return result