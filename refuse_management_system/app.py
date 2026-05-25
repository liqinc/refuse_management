import os
from flask import Flask, render_template, redirect, url_for

# 导入扩展实例
from extensions import db, bcrypt, login_manager, migrate
from flask_login import login_required

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 初始化Flask应用
app = Flask(__name__, template_folder=os.path.join(basedir, 'app_package', 'templates'), static_folder=os.path.join(basedir, 'app_package', 'static'))

# 打印模板和静态文件目录路径，用于调试
print(f"Template folder: {app.template_folder}")
print(f"Static folder: {app.static_folder}")

# 配置应用
app.config['SECRET_KEY'] = '123456'  # 生产环境应使用环境变量
# MySQL数据库配置
# 格式: mysql+pymysql://username:password@hostname/database_name
# 根据工作区上下文，使用密码123456连接MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/refuse_management'
# 如果MySQL服务器密码不是123456，请修改上面的密码
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    # 在函数内部导入模型，避免循环导入
    from app_package.models import User
    return User.query.get(int(user_id))

# 首页路由
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# 更新dashboard路由以提供数据
@app.route('/dashboard')
@login_required
def dashboard():
    from datetime import datetime
    
    # 在函数内部导入模型，避免循环导入
    from app_package.models import RefuseType, RefuseCategory, RefuseNews, User
    
    # 获取统计数据
    refuse_type_count = RefuseType.query.count()
    refuse_category_count = RefuseCategory.query.count()
    refuse_news_count = RefuseNews.query.count()
    user_count = User.query.count()
    
    # 获取最新3条资讯
    recent_news = RefuseNews.query.order_by(RefuseNews.publish_date.desc()).limit(3).all()
    
    return render_template('auth/dashboard.html',
                          now=datetime.now(),
                          refuse_type_count=refuse_type_count,
                          refuse_category_count=refuse_category_count,
                          refuse_news_count=refuse_news_count,
                          user_count=user_count,
                          recent_news=recent_news)

# 导入模型和路由
from app_package.routes import auth, refuse_type, refuse_category, refuse_news, user_profile

# 注册蓝图
app.register_blueprint(auth.bp)
app.register_blueprint(refuse_type.bp)
app.register_blueprint(refuse_category.bp)
app.register_blueprint(refuse_news.bp)
app.register_blueprint(user_profile.bp)

if __name__ == '__main__':
    # 在开发环境下运行应用
    app.run(port=5001, debug=True)