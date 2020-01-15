# FisrtFlask
使用Python3.6+pycharm+mysql+flask搭建的简单web网站，含认证授权，日志打印，异常处理，事务提交与回滚，参数验证，文件上传下载，图片预览，<br/>
ssh连接服务器执行命令等功能，包含用户管理与企业管理两块。目前没有页面<br/>
初始用户名admin，密码admin，可通过用户管理进行添加删除修改查询<br/>
使用用户名密码登录后生成token，(https://github.com/t-lixiang1995/FisrtFlask/blob/master/static/img/%E7%99%BB%E5%BD%95.jpg) <br/>
每次请求带上token即可，(https://github.com/t-lixiang1995/FisrtFlask/blob/master/static/img/%E8%AF%B7%E6%B1%82.jpg) <br/>
使用以下3条命令进行数据库初始化：<br/>
    python manage.py db init <br/>
    python manage.py db migrate <br/>
    python manage.py db upgrade <br/>
使用：python manage.py runserver启动服务，若提示有模块没安装，使用pip install命令安装即可。