# -*- coding: utf-8 -*-
"""
数据库初始化脚本 - 使用MySQL数据库

此脚本负责初始化垃圾分类系统的MySQL数据库，包括：
1. 创建数据库表
2. 初始化管理员用户
3. 添加示例数据

脚本支持两种初始化方式：ORM和SQL脚本
"""

import os
import sys
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加当前目录到Python路径，确保可以导入app模块
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


class DatabaseConfig:
    """数据库配置类"""
    # 数据库连接配置
    DB_USERNAME = 'root'
    DB_PASSWORD = '123456'
    DB_HOST = 'localhost'
    DB_NAME = 'refuse_management'
    
    # Flask应用配置
    SECRET_KEY = '123456'
    
    @classmethod
    def get_db_url(cls):
        """构建并返回数据库连接URL"""
        return f"mysql+pymysql://{cls.DB_USERNAME}:{cls.DB_PASSWORD}@{cls.DB_HOST}/{cls.DB_NAME}?charset=utf8mb4"


def create_temp_app():
    """创建临时Flask应用实例"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = DatabaseConfig.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfig.get_db_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 配置SQLAlchemy日志级别
    app.logger.setLevel(logging.INFO)
    
    return app


# 创建临时Flask应用实例
temp_app = create_temp_app()

# 创建数据库实例
db = SQLAlchemy(temp_app)


# 定义数据库模型
class RefuseType(db.Model):
    """垃圾类型模型"""
    __tablename__ = 'refuse_types'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True, comment='垃圾类型名称')
    description = db.Column(db.Text, comment='类型描述')
    icon_url = db.Column(db.String(500), comment='图标URL')
    color = db.Column(db.String(7), default='#1296db', comment='类型颜色')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系定义
    categories = db.relationship('RefuseCategory', backref='refuse_type', lazy=True, cascade='all, delete-orphan')


class RefuseCategory(db.Model):
    """垃圾分类模型"""
    __tablename__ = 'refuse_categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('refuse_types.id', ondelete='CASCADE'), nullable=False, comment='垃圾类型ID')
    category_name = db.Column(db.String(100), nullable=False, comment='垃圾名称')
    description = db.Column(db.Text, comment='垃圾描述')
    sorting_guide = db.Column(db.Text, comment='分类指南')
    image_url = db.Column(db.String(500), comment='图片URL')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 联合唯一约束
    __table_args__ = (db.UniqueConstraint('category_name', 'type_id', name='unique_category_type'),)


class RefuseNews(db.Model):
    """垃圾资讯模型"""
    __tablename__ = 'refuse_news'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment='资讯标题')
    subtitle = db.Column(db.String(255), comment='副标题')
    publish_date = db.Column(db.Date, nullable=False, default=datetime.now().date, comment='发布日期')
    author = db.Column(db.String(100), comment='作者')
    source = db.Column(db.String(100), comment='来源')
    views = db.Column(db.Integer, default=0, comment='浏览量')
    likes = db.Column(db.Integer, default=0, comment='点赞数')
    category = db.Column(db.String(50), comment='分类')
    cover_image = db.Column(db.String(500), comment='封面图片URL')
    content = db.Column(db.Text, nullable=False, comment='资讯内容')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='邮箱')
    role = db.Column(db.Enum('admin', 'user'), default='user', comment='用户角色')
    avatar = db.Column(db.String(500), comment='头像URL')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def set_password(self, password):
        """设置密码（注意：生产环境应使用密码哈希）"""
        # 当前为演示版本，直接存储明文密码
        self.password = password
    
    def check_password(self, password):
        """验证密码"""
        return self.password == password
    
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'

def _validate_mysql_connection():
    """验证MySQL数据库连接"""
    try:
        logger.info("测试数据库连接...")
        with db.engine.connect() as conn:
            conn.execute(db.text("SELECT 1"))
        logger.info("数据库连接成功！")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return False


def _validate_password_strength(password):
    """验证密码强度"""
    # 基本的密码强度检查
    if len(password) < 6:
        logger.warning("警告：密码强度较弱，建议至少6个字符")
    return True


def init_database_with_orm():
    """使用SQLAlchemy ORM初始化数据库"""
    logger.info("开始使用ORM方式初始化数据库...")
    
    try:
        # 验证数据库连接
        if not _validate_mysql_connection():
            return False
        
        # 创建数据库表
        logger.info("创建数据库表...")
        db.create_all()
        logger.info("数据库表创建成功")
        
        # 检查管理员用户是否已存在
        existing_admin = User.query.filter_by(username='admin').first()
        
        if not existing_admin:
            # 初始化管理员用户
            logger.info("创建管理员用户...")
            admin_password = 'admin123'
            _validate_password_strength(admin_password)
            
            admin = User(
                username='admin', 
                email='admin@example.com', 
                role='admin',
                is_active=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            
            # 添加一些示例数据
            logger.info("添加示例垃圾类型数据...")
            
            # 添加垃圾类型
            recyclable = RefuseType(
                type_name='可回收物', 
                description='可循环利用的废弃物',
                color='#4CAF50'
            )
            hazardous = RefuseType(
                type_name='有害垃圾', 
                description='对人体健康或自然环境造成直接或潜在危害的生活废弃物',
                color='#F44336'
            )
            kitchen = RefuseType(
                type_name='厨余垃圾', 
                description='居民日常生活及食品加工、饮食服务、单位供餐等活动中产生的垃圾',
                color='#FF9800'
            )
            other = RefuseType(
                type_name='其他垃圾', 
                description='除可回收物、有害垃圾、厨余垃圾以外的其他生活废弃物',
                color='#9E9E9E'
            )
            
            db.session.add_all([recyclable, hazardous, kitchen, other])
            db.session.flush()  # 获取ID但不提交
            
            # 添加垃圾类别
            logger.info("添加示例垃圾分类数据...")
            
            paper = RefuseCategory(
                category_name='纸类', 
                description='报纸、杂志、书籍、各种包装纸等', 
                type_id=recyclable.id,
                sorting_guide='尽量保持清洁干燥，避免污染'
            )
            plastic = RefuseCategory(
                category_name='塑料', 
                description='各种塑料袋、塑料瓶、泡沫塑料等', 
                type_id=recyclable.id,
                sorting_guide='请清洗并压扁，减少体积'
            )
            metal = RefuseCategory(
                category_name='金属', 
                description='各种废金属物品', 
                type_id=recyclable.id,
                sorting_guide='请去除残留物，保持干燥'
            )
            battery = RefuseCategory(
                category_name='电池', 
                description='各类废电池', 
                type_id=hazardous.id,
                sorting_guide='请放入专门的有害垃圾回收箱'
            )
            electronics = RefuseCategory(
                category_name='电子产品', 
                description='废手机、电脑等电子产品', 
                type_id=hazardous.id,
                sorting_guide='请回收至专门的电子废弃物回收点'
            )
            
            db.session.add_all([paper, plastic, metal, battery, electronics])
            db.session.commit()
            
            logger.info("数据库初始化完成！")
            logger.info("管理员账号: admin")
            logger.info("管理员密码: admin123 (建议首次登录后修改)")
        else:
            logger.info("数据库已初始化，管理员用户已存在。")
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"使用ORM初始化数据库失败: {str(e)}")
        return False


def init_database_with_sql():
    """使用SQL脚本初始化数据库"""
    logger.info("开始使用SQL脚本方式初始化数据库...")
    
    try:
        # 验证数据库连接
        if not _validate_mysql_connection():
            return False
        
        # 读取SQL脚本文件
        sql_file_path = os.path.join(os.path.dirname(__file__), 'sql', 'create_tables.sql')
        if not os.path.exists(sql_file_path):
            logger.error(f"未找到SQL脚本文件: {sql_file_path}")
            return False
            
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
            
        # 分割SQL命令
        commands = sql_commands.split(';')
        
        # 执行SQL命令
        logger.info("执行SQL脚本创建数据库表...")
        with db.engine.connect() as connection:
            with connection.begin() as transaction:
                try:
                    for command in commands:
                        command = command.strip()
                        if command:
                            connection.execute(db.text(command))
                    transaction.commit()
                    logger.info("SQL脚本执行成功，数据库表已创建！")
                except Exception as e:
                    transaction.rollback()
                    logger.error(f"SQL脚本执行失败: {str(e)}")
                    return False
        
        # 手动创建管理员用户（因为SQL脚本没有包含这部分）
        logger.info("创建管理员用户...")
        admin_password = 'admin123'
        _validate_password_strength(admin_password)
        
        with db.engine.connect() as connection:
            with connection.begin() as transaction:
                try:
                    # 检查管理员是否已存在
                    result = connection.execute(db.text("SELECT COUNT(*) FROM users WHERE username = 'admin'"))
                    if result.scalar() == 0:
                        # 创建管理员用户
                        connection.execute(
                            db.text("INSERT INTO users (username, email, password, role, is_active) VALUES (:username, :email, :password, :role, :is_active)"),
                            {
                                "username": "admin", 
                                "email": "admin@example.com", 
                                "password": admin_password, 
                                "role": "admin", 
                                "is_active": True
                            }
                        )
                        logger.info("管理员用户创建成功！")
                        logger.info("管理员账号: admin")
                        logger.info("管理员密码: admin123 (建议首次登录后修改)")
                    else:
                        logger.info("管理员用户已存在。")
                    transaction.commit()
                except Exception as e:
                    transaction.rollback()
                    logger.error(f"创建管理员用户失败: {str(e)}")
                    return False
                    
        return True
    except Exception as e:
        logger.error(f"使用SQL脚本初始化数据库失败: {str(e)}")
        return False


def print_manual_instructions():
    """打印手动初始化数据库的说明"""
    print("\n您也可以尝试手动初始化数据库：")
    print("1. 确保已创建refuse_management数据库")
    print("2. 使用MySQL命令行或工具执行sql/create_tables.sql脚本")
    print("3. 手动创建管理员用户：")
    print("   INSERT INTO users (username, email, password, role, is_active) VALUES ('admin', 'admin@example.com', 'admin123', 'admin', 1);")


if __name__ == '__main__':
    # 使用应用上下文执行数据库操作
    with temp_app.app_context():
        print("\n=====================")
        print("MySQL数据库初始化工具")
        print("=====================")
        print(f"连接数据库: {DatabaseConfig.DB_USERNAME}@{DatabaseConfig.DB_HOST}/{DatabaseConfig.DB_NAME}")
        
        try:
            # 先尝试使用ORM方式初始化
            if init_database_with_orm():
                print("\n数据库初始化成功！")
            else:
                # 如果ORM方式失败，尝试使用SQL脚本方式
                print("\n尝试使用SQL脚本方式初始化数据库...")
                if init_database_with_sql():
                    print("\n数据库初始化成功！")
                else:
                    print("\n数据库初始化失败！")
                    print("请检查MySQL服务器是否运行，以及连接信息是否正确。")
                    print_manual_instructions()
        except Exception as e:
            logger.error(f"数据库初始化过程发生错误: {str(e)}")
            print(f"\n数据库初始化过程发生错误: {str(e)}")
            print("\n请检查MySQL服务器是否运行，以及连接信息是否正确。")
            print_manual_instructions()