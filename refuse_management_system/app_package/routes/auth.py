from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
from extensions import db
from datetime import datetime

# 创建认证蓝图
bp = Blueprint('auth', __name__)

# 注册路由
@bp.route('/register', methods=['GET', 'POST'])
def register():
    from app_package.models import User
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
        
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验证表单数据
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'danger')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return redirect(url_for('auth.register'))
            
        # 创建新用户 - 使用明文密码
        user = User(username=username, email=email)
        user.set_password(password)  # 现在set_password方法直接存储明文密码
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('注册失败，请稍后再试', 'danger')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

# 登录路由
@bp.route('/login', methods=['GET', 'POST'])
def login():
    from app_package.models import User
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
        
    if request.method == 'POST':
        # 获取表单数据 - 注意模板中使用的是username字段
        login_id = request.form.get('username')  # 可以是邮箱或用户名
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        # 尝试通过邮箱查找用户
        user = User.query.filter_by(email=login_id).first()
        
        # 如果没有找到，尝试通过用户名查找
        if not user:
            user = User.query.filter_by(username=login_id).first()
        
        # 验证用户和密码
        if user:
            if not user.is_active:
                flash('用户未激活，请联系管理员', 'danger')
            elif user.check_password(password):  # 现在check_password方法直接比较明文
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))
            else:
                flash('登录失败，密码错误', 'danger')
        else:
            flash('登录失败，未找到该用户', 'danger')
            
        return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

# 登出路由
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))

# 仪表盘路由
@bp.route('/dashboard')
@login_required
def dashboard():
    from datetime import datetime
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