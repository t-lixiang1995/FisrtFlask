# @Time : 2019/10/21 10:26
# @Author : lixiang
# @File : _init_.py
# @Software: PyCharm
import os

from flask import g

from app.models.user import User, Role

#权限验证方法
def very_permission(permissionCode):
    curruser = User.query.filter(User.accName == g.user).first()
    currrole = Role.query.filter(Role.id == curruser.role_id).first()
    roleToResourceS = currrole.participateResource.all()
    # print(role.participateResource.all())
    for roleToResource in roleToResourceS:
        if permissionCode == roleToResource.id:
            return True
    return False


# 根据路径和文件名读取文件内容
def readFileContent(path,fileName):
    pathTmp = os.path.join(path, fileName)                # 获取path与filename组合后的路径
    try:
        fp = open(pathTmp,"r")                            #打开文件
        confBuffer = fp.read()                            #读取文件
        fp.close()
        return confBuffer
    except IOError as ioe:
        print(ioe)


# 根据全路径和文件内容写入文件
def wirteFileContent(FullPath,configContent):
    try:
        fp = open(FullPath,"w")                            #打开文件
        fp.write(configContent)
        fp.close()
    except IOError as ioe:
        print(ioe)