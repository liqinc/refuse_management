# -*- coding: utf-8 -*-
"""数据库连接和用户表验证脚本"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# 添加当前目录到Python路径
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 创建临时Flask应用
app = Flask(__name__)

# 配置MySQL数据库（与app.py保持一致）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/refuse_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库实例
db = SQLAlchemy(app)

# 定义User模型（与实际项目一致）
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # 与数据库字段一致
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'user'), default='user')
    avatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password):
        """验证用户密码 - 直接比较明文"""
        return self.password == password

# 验证密码函数
def verify_user(username, password):
    """验证用户凭据"""
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"找到用户: {user.username}, 邮箱: {user.email}, 角色: {user.role}, 激活状态: {user.is_active}")
        print(f"密码: {user.password}")
        is_valid = user.check_password(password)  # 使用模型中的密码验证方法
        print(f"密码验证结果: {'成功' if is_valid else '失败'}")
        return is_valid
    else:
        print(f"未找到用户: {username}")
        return False

# 检查数据库表结构
def check_database_structure():
    """检查数据库表结构"""
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    # 检查数据库是否包含users表
    tables = inspector.get_table_names()
    print("\n数据库中的表:")
    for table in tables:
        print(f"- {table}")
    
    # 检查users表的字段
    if 'users' in tables:
        print("\nusers表的字段:")
        columns = inspector.get_columns('users')
        for column in columns:
            print(f"- {column['name']} ({column['type']})"
                  f"{' (主键)' if column.get('primary_key') else ''}"
                  f"{' (非空)' if not column.get('nullable') else ''}")
    
    # 检查索引
    if 'users' in tables:
        print("\nusers表的索引:")
        indexes = inspector.get_indexes('users')
        for index in indexes:
            print(f"- {index['name']}: 列={index['column_names']}, 唯一={index['unique']}")

# 使用应用上下文
with app.app_context():
    try:
        # 检查数据库连接
        print("测试数据库连接...")
        connection = db.engine.connect()
        print("数据库连接成功！")
        connection.close()
        
        # 检查数据库结构
        check_database_structure()
        
        # 查询所有用户
        print("\n查询所有用户:")
        users = User.query.all()
        for user in users:
            print(f"用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 角色: {user.role}")
        
        # 验证admin用户
        print("\n验证admin用户凭据:")
        admin_username = 'admin'
        admin_password = 'admin123'
        verify_user(admin_username, admin_password)
        
        print("\n测试完成！")
        print("\n如果登录仍然失败，请检查以下几点:")
        print("1. auth.py中的登录逻辑是否正确处理了密码验证")
        print("2. 用户模型中的is_active字段是否为True")
        print("3. Flask-Login的配置是否正确")
        
    except Exception as e:
        print(f"操作失败: {str(e)}")
        print("\n请检查MySQL服务器是否运行，以及连接信息是否正确。")
        print("如果问题仍然存在，请重新运行reset_admin_user.py脚本重置管理员用户。")