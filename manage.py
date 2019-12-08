from flask_script import Manager,Server
from flask_migrate import MigrateCommand, Migrate
from app import create_app, db

app= create_app()
manager = Manager(app)
migrate = Migrate(app, db)

"""
# 数据库迁移命名
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
"""
# 5.3 创建db命令，以后在数据库操作的时候都可使用db
manager.add_command('db', MigrateCommand)

"""
# 自定义命令
    python manage.py runserver 
"""
manager.add_command("runserver", Server(host='0.0.0.0', port=8899))

"""
生成当前环境的所有依赖： requirements.txt
    pip3 freeze > requirements.txt

生成当前程序的所有依赖： requirements.txt
    pip3 install pipreqs
    pipreqs ./

"""

if __name__ == "__main__":
    manager.run()