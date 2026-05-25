from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime

# 创建用户个人中心蓝图
bp = Blueprint('user_profile', __name__, url_prefix='/profile')

# 查看个人资料
@bp.route('/')
@login_required
def profile():
    return render_template('user_profile/profile.html', user=current_user)

# 编辑个人资料
@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from app_package.models import User
    if request.method == 'POST':
        # 获取表单数据
        email = request.form.get('email')
        avatar = request.form.get('avatar')
        
        # 验证邮箱
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash('该邮箱已被使用', 'danger')
            return redirect(url_for('user_profile.edit_profile'))
            
        # 更新个人资料
        current_user.email = email
        current_user.avatar = avatar
        current_user.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('个人资料更新成功', 'success')
            return redirect(url_for('user_profile.profile'))
        except Exception as e:
            db.session.rollback()
            flash('个人资料更新失败，请稍后再试', 'danger')
            return redirect(url_for('user_profile.edit_profile'))
            
    return render_template('user_profile/edit.html', user=current_user)

# 修改密码
@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        # 获取表单数据
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        
        # 验证当前密码
        if not current_user.check_password(current_password):
            flash('当前密码不正确', 'danger')
            return redirect(url_for('user_profile.change_password'))
            
        # 验证新密码
        if new_password != confirm_new_password:
            flash('两次输入的新密码不一致', 'danger')
            return redirect(url_for('user_profile.change_password'))
            
        # 更新密码
        current_user.set_password(new_password)
        current_user.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('密码修改成功，请重新登录', 'success')
            return redirect(url_for('auth.logout'))
        except Exception as e:
            db.session.rollback()
            flash('密码修改失败，请稍后再试', 'danger')
            return redirect(url_for('user_profile.change_password'))
            
    return render_template('user_profile/change_password.html')

# 管理用户列表（仅管理员可见）
@bp.route('/users')
@login_required
def manage_users():
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('auth.dashboard'))
        
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('user_profile/manage_users.html', users=users)

# 禁用/启用用户（仅管理员）
@bp.route('/toggle-status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.is_admin() or user_id == current_user.id:
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('user_profile.manage_users'))
        
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    user.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        status = '启用' if user.is_active else '禁用'
        flash(f'用户 {user.username} 已{status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('操作失败，请稍后再试', 'danger')
        
    return redirect(url_for('user_profile.manage_users'))

# 删除用户（仅管理员）
@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin() or user_id == current_user.id:
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('user_profile.manage_users'))
        
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'用户 {user.username} 已删除', 'success')
    except Exception as e:
        db.session.rollback()
        flash('用户删除失败，请稍后再试', 'danger')
        
    return redirect(url_for('user_profile.manage_users'))