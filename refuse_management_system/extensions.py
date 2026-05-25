#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""扩展模块，用于存储数据库和其他Flask扩展实例，避免循环导入"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

# 创建数据库实例
db = SQLAlchemy()

# 创建加密实例
bcrypt = Bcrypt()

# 创建登录管理实例
login_manager = LoginManager()

# 创建迁移实例
migrate = Migrate()