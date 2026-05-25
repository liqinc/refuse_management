# 垃圾分类管理系统

一个基于Flask的垃圾分类管理系统，用于管理垃圾类型、垃圾分类、垃圾资讯和用户信息，提供友好的Web界面和完整的管理功能。

## 项目结构

```
refuse_management_system/
├── app.py                 # 应用主入口
├── requirements.txt       # 项目依赖
├── db_init_mysql.py       # 数据库初始化脚本
├── create_mysql_db.py     # MySQL数据库创建脚本
├── make_admin.py          # 管理员账号创建脚本
├── extensions.py          # Flask扩展配置
├── sql/
│   └── create_tables.sql  # 数据库表创建语句
├── migrations/            # 数据库迁移文件
└── app_package/
    ├── __init__.py        # 包初始化
    ├── models.py          # 数据库模型
    ├── routes/            # 路由模块
    │   ├── auth.py        # 认证相关路由
    │   ├── refuse_type.py # 垃圾类型管理
    │   ├── refuse_category.py # 垃圾分类管理
    │   ├── refuse_news.py # 垃圾资讯管理
    │   └── user_profile.py # 用户管理
    ├── static/            # 静态资源(CSS, JS, 图片)
    └── templates/         # HTML模板
        ├── base.html      # 基础模板
        ├── dashboard.html # 仪表盘模板
        ├── auth/
        ├── refuse_type/
        ├── refuse_category/
        ├── refuse_news/
        └── user_profile/
```

## 功能特性

- **用户认证系统**
  - 用户注册、登录、登出功能
  - 基于角色的权限控制（普通用户/管理员）
  - 个人资料管理

- **垃圾类型管理**
  - 添加、编辑、删除垃圾类型
  - 设置类型名称、描述、图标URL和颜色
  - 类型唯一性验证

- **垃圾分类管理**
  - 分类的增删改查操作
  - 详细的分类描述和回收指南
  - 按垃圾类型分类浏览

- **垃圾资讯管理**
  - 垃圾分类相关资讯发布和管理
  - 资讯详情查看

- **数据可视化**
  - 仪表盘数据统计展示
  - 各类数据概览卡片

- **前端交互功能**
  - 颜色选择器组件
  - 表单数据验证
  - 响应式设计适配不同设备

## 环境要求

- **Python**: 3.7 或更高版本
- **Web框架**: Flask 2.0+
- **数据库**: MySQL 5.7+ (主要支持)
- **ORM框架**: SQLAlchemy 1.4+
- **认证**: Flask-Login
- **密码处理**: Flask-Bcrypt
- **数据库迁移**: Flask-Migrate

## 数据库模型

系统包含四个主要数据模型：

- **RefuseType**: 垃圾类型表，存储各类垃圾的基本信息和颜色配置
- **RefuseCategory**: 垃圾分类表，关联到垃圾类型，存储详细分类信息
- **RefuseNews**: 垃圾资讯表，存储相关新闻和公告
- **User**: 用户表，存储用户信息和权限

## 安装说明

1. 克隆项目代码（如果适用）

```bash
git clone <repository_url>
cd refuse_management_system
```

2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置数据库

编辑以下文件中的数据库连接信息：

- **app.py**: 应用运行时的数据库配置
- **db_init_mysql.py**: 数据库初始化时的配置

默认配置示例：
```python
# MySQL数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/refuse_management'
```

5. 创建数据库（如果尚未创建）

```bash
# 执行数据库创建脚本
python create_mysql_db.py
```

6. 初始化数据库

可以使用自动化脚本来初始化数据库表和添加初始数据：

```bash
# 使用初始化脚本（推荐）
python db_init_mysql.py
```

或者使用数据库迁移工具：

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

或者直接执行SQL脚本：

```bash
mysql -u root -p refuse_management < sql/create_tables.sql
```

7. 运行应用

```bash
# 方法一：使用Python直接运行
python app.py

# 方法二：使用Flask命令
flask run

# Windows环境变量设置
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

## 使用指南

### 访问系统
- 启动应用后，访问 http://localhost:5000 打开系统

### 账户管理
- 可以注册新账户或使用现有账户登录
- 初始管理员账户：admin/admin123（由db_init_mysql.py脚本自动创建）

### 系统角色
- **普通用户**：可查看垃圾分类和资讯信息
- **管理员**：可访问所有管理功能

### 功能使用

#### 垃圾类型管理
1. 登录系统后，在左侧菜单选择"垃圾类型管理"
2. 点击"添加垃圾类型"按钮创建新类型
3. 使用颜色选择器设置类型颜色
4. 可以编辑或删除已存在的类型

#### 垃圾分类管理
1. 在左侧菜单选择"垃圾分类管理"
2. 可以按垃圾类型筛选分类
3. 点击"添加垃圾分类"按钮创建新分类
4. 填写详细信息和分类指南

#### 垃圾资讯管理
1. 在左侧菜单选择"垃圾资讯管理"
2. 点击"发布资讯"按钮添加新资讯
3. 填写标题、内容等信息

## 注意事项

### 安全性说明
- **开发版本警告**：当前版本为演示版本，使用明文密码存储
- **生产环境要求**：部署到生产环境前，请确保：
  - 配置复杂的SECRET_KEY
  - 启用密码加密存储
  - 配置HTTPS
  - 限制管理员账户访问

### 数据维护
- 定期备份数据库
- 建议使用定时任务备份重要数据

### 性能优化
- 大量数据时考虑添加数据库索引
- 可以调整SQLALCHEMY_ECHO设置以进行性能调试

### 部署建议
- 生产环境推荐使用Gunicorn或uWSGI作为WSGI服务器
- 配置Nginx作为反向代理
- 使用supervisor管理进程
- 参考Flask官方文档的部署指南获取更详细信息

## 许可证

[MIT](https://opensource.org/licenses/MIT)

## 联系方式

如有任何问题或建议，请联系项目维护者。

*本项目仅供学习和教学使用，实际应用请进行必要的安全加固。*