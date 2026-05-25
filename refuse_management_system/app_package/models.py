
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from extensions import db

# 垃圾类型模型 - 根据数据库实际结构修复
class RefuseType(db.Model):
    __tablename__ = 'refuse_types'  # 数据库中实际的表名是 refuse_types，不是 refuse_type
    
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)  # 数据库中实际的字段名是 type_name，不是 name
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(255))  # 数据库中实际有这个字段
    color = db.Column(db.String(20), default='#999999')  # 添加颜色字段，默认灰色
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：一个垃圾类型可以对应多个垃圾
    categories = db.relationship('RefuseCategory', backref='refuse_type', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<RefuseType {self.type_name}>'

# 垃圾分类模型 - 根据数据库实际结构修复
class RefuseCategory(db.Model):
    __tablename__ = 'refuse_categories'  # 数据库中实际的表名是 refuse_categories，不是 refuse_category
    
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('refuse_types.id'), nullable=False)  # 外键引用实际的表名
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sorting_guide = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 添加联合唯一约束
    __table_args__ = (db.UniqueConstraint('category_name', 'type_id'),)
    
    def __repr__(self):
        return f'<RefuseCategory {self.category_name}>'

# 垃圾资讯模型 - 根据数据库实际结构修复
class RefuseNews(db.Model):
    __tablename__ = 'refuse_news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # 更新字段长度
    subtitle = db.Column(db.String(255))  # 新增副标题字段
    publish_date = db.Column(db.Date, nullable=False)  # 发布日期
    author = db.Column(db.String(100))  # 更新字段长度
    source = db.Column(db.String(100))  # 新增来源字段
    views = db.Column(db.Integer, default=0)  # 浏览量
    likes = db.Column(db.Integer, default=0)  # 新增点赞数字段
    category = db.Column(db.String(50))  # 新增分类字段
    cover_image = db.Column(db.String(255), name='coverImage')  # 封面图片，映射到数据库中的coverImage字段
    content = db.Column(db.Text, nullable=False)  # 资讯内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    def __repr__(self):
        return f'<RefuseNews {self.title}>'

# 用户模型 - 根据数据库实际结构修复
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 数据库中实际的表名是 users，不是 user
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # 使用明文密码
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'user'), default='user')
    avatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """设置用户密码 - 不加密，直接存储明文"""
        self.password = password
        
    def check_password(self, password):
        """验证用户密码 - 直接比较明文"""
        return self.password == password
        
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'
