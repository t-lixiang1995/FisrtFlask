# 前言

基于Flask搭建的web网站。(Python3.6+Pycharm2019.2+Mysql8.0+Flask.1.1)

> 🔥 ：项目目前提供基础web网站功能，后续会持续更新。

1. 认证授权
2. 日志打印
3. 异常处理
4. 事务
5. 参数校验
6. 文件操作
7. 服务器静态资源访问
8. ssh连接服务器执行命令
9. 用户管理
9. 企业管理
-------

目前的项目结构如下：

```
[-] xxx
  ├──[-] FirstFlask-app-models      // 数据库表定义。
  ├──[-] FirstFlask-app-routes      // 视图。
  ├──[-] FirstFlask-app-__init__    // token校验,异常处理,注册蓝图
  ├──[-] FirstFlask-common          // 全局异常声明，线程池参数设置，数据操纵方法定义，格式转换工具
  ├──[-] FirstFlask-settings        // 全局配置。
```

## 使用的主要框架
| 框架 | 说明 |  版本 |
| --- | --- | --- |
| [Flask](https://flask.palletsprojects.com/en/1.1.x/) | 主框架 | 1.1.1 |
| [flask_httpauth](https://flask.palletsprojects.com/en/1.1.x/) | 认证 | 3.3.0 |
| [paramiko](http://www.paramiko.org/) | 使用使用SSHv2协议连接服务器 | 2.7.1 |
| [pymysql](https://pypi.org/project/PyMySQL/) | 连接mysql数据库 | 0.9.3 |
| [itsdangerous](https://itsdangerous.palletsprojects.com/en/1.1.x/) | 签名模块 | 3.11.0 |
| [passlib](https://pythonhosted.org/passlib/) | 密码散列库 | 1.7.1 |

#### 项目运行流程
#####
    1.python manage.py db init
    2.python manage.py db migrate
    3.python manage.py db upgrade
    4.启动服务：python manage.py runserver
    5.浏览器输入http://127.0.0.1:8899/sys/login使用初始账户admin,admin登录，之后所有请求带上登录生成的token即可
* 登录如下图：![登录](https://github.com/t-lixiang1995/FisrtFlask/blob/master/static/img/%E7%99%BB%E5%BD%95.jpg)
* 请求如下图：![请求](https://github.com/t-lixiang1995/FisrtFlask/blob/master/static/img/%E8%AF%B7%E6%B1%82.jpg)