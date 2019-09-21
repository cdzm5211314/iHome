# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-17 22:27


from iHome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand  # 迁移的执行者与迁移的解析命令

# 创建flask的应用对象
app = create_app('develop')

# 创建启动脚本命令管理类对象
manager = Manager(app)

# 创建迁移者对象,需要保存到app当中且会用到数据库db
Migrate(app, db)

# 向manager对象中添加数据库的操作命令
# 此处db与数据库SQLAlchemy工具对象db不是一个意思,这个db只是操作命令的一个命令名字
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()
    # 终端命令操作:
    # 1.创建迁移仓库(初始化): python manage.py db init
    # 2.创建迁移文件: python manage.py db migrate -m "init table"
    # 3.更新数据库: python manage.py db upgrade

    # 后端视图开发的一般套路步骤: 如下
    # 1.获取参数
    # 2.校验参数
    # 3.业务逻辑处理
    # 4.返回值
