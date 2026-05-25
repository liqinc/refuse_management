from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime
from flask import jsonify, request

# 创建垃圾类型管理蓝图
bp = Blueprint('refuse_type', 'refuse_type', url_prefix='/refuse-type')

# 列表所有垃圾类型
@bp.route('/')
@login_required
def list_types():
    from app_package.models import RefuseType
    types = RefuseType.query.order_by(RefuseType.created_at.desc()).all()
    return render_template('refuse_type/list.html', types=types)

# 添加新垃圾类型
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_type():
    from app_package.models import RefuseType
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_type.list_types'))
        
    if request.method == 'POST':
        # 获取表单数据
        type_name = request.form.get('type_name')
        description = request.form.get('description')
        icon_url = request.form.get('icon_url')
        color = request.form.get('color')
        
        # 验证数据
        if RefuseType.query.filter_by(type_name=type_name).first():
            flash('垃圾类型名称已存在', 'danger')
            return redirect(url_for('refuse_type.add_type'))
            
        # 创建新垃圾类型
        refuse_type = RefuseType(
            type_name=type_name,
            description=description,
            icon_url=icon_url,
            color=color
        )
        
        try:
            db.session.add(refuse_type)
            db.session.commit()
            flash('垃圾类型添加成功', 'success')
            return redirect(url_for('refuse_type.list_types'))
        except Exception as e:
            db.session.rollback()
            flash('垃圾类型添加失败，请稍后再试', 'danger')
            return redirect(url_for('refuse_type.add_type'))
            
    return render_template('refuse_type/add.html')

# 编辑垃圾类型
@bp.route('/edit/<int:type_id>', methods=['GET', 'POST'])
@login_required
def edit_type(type_id):
    from app_package.models import RefuseType
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_type.list_types'))
        
    refuse_type = RefuseType.query.get_or_404(type_id)
    
    if request.method == 'POST':
        # 获取表单数据
        type_name = request.form.get('type_name')
        description = request.form.get('description')
        icon_url = request.form.get('icon_url')
        color = request.form.get('color')
        
        # 验证数据（除了当前记录外，不允许有重复的类型名称）
        existing_type = RefuseType.query.filter_by(type_name=type_name).first()
        if existing_type and existing_type.id != type_id:
            flash('垃圾类型名称已存在', 'danger')
            return redirect(url_for('refuse_type.edit_type', type_id=type_id))
            
        # 更新垃圾类型
        refuse_type.type_name = type_name
        refuse_type.description = description
        refuse_type.icon_url = icon_url
        refuse_type.color = color
        refuse_type.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('垃圾类型更新成功', 'success')
            return redirect(url_for('refuse_type.list_types'))
        except Exception as e:
            db.session.rollback()
            flash('垃圾类型更新失败，请稍后再试', 'danger')
            return redirect(url_for('refuse_type.edit_type', type_id=type_id))
            
    return render_template('refuse_type/edit.html', type=refuse_type)

# 删除垃圾类型
@bp.route('/delete/<int:type_id>', methods=['POST'])
@login_required
def delete_type(type_id):
    from app_package.models import RefuseType
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_type.list_types'))
        
    refuse_type = RefuseType.query.get_or_404(type_id)
    
    try:
        db.session.delete(refuse_type)
        db.session.commit()
        flash('垃圾类型删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash('垃圾类型删除失败，可能有相关的垃圾记录', 'danger')
        
    return redirect(url_for('refuse_type.list_types'))

# 查看垃圾类型详情
@bp.route('/detail/<int:type_id>')
@login_required
def detail_type(type_id):
    from app_package.models import RefuseType
    refuse_type = RefuseType.query.get_or_404(type_id)
    return render_template('refuse_type/detail.html', type=refuse_type)

# 批量删除垃圾类型
@bp.route('/batch-delete', methods=['POST'])
@login_required
def batch_delete_types():
    from app_package.models import RefuseType
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_type.list_types'))
    
    type_ids = request.form.getlist('type_ids')
    if not type_ids:
        flash('请至少选择一个垃圾类型进行删除', 'danger')
        return redirect(url_for('refuse_type.list_types'))
    
    try:
        # 将字符串ID转换为整数
        type_ids = [int(id) for id in type_ids]
        # 删除选中的垃圾类型
        RefuseType.query.filter(RefuseType.id.in_(type_ids)).delete(synchronize_session=False)
        db.session.commit()
        flash(f'成功删除 {len(type_ids)} 个垃圾类型', 'success')
    except Exception as e:
        db.session.rollback()
        flash('批量删除失败，可能有相关的垃圾记录', 'danger')
    
    return redirect(url_for('refuse_type.list_types'))

# API接口：获取所有垃圾类型（JSON格式，供微信小程序调用）
@bp.route('/api/list')
def api_list_types():
    from app_package.models import RefuseType
    
    try:
        # 查询所有垃圾类型
        refuse_types = RefuseType.query.all()
        
        # 定义默认颜色映射（根据常见的垃圾分类颜色）作为备选
        default_colors = {
            '可回收物': '#1296db',  # 蓝色
            '有害垃圾': '#ff6b6b',  # 红色
            '厨余垃圾': '#4ecdc4',  # 绿色
            '其他垃圾': '#a8dadc',  # 灰色
        }
        
        # 将查询结果转换为字典列表
        types_list = []
        for refuse_type in refuse_types:
            # 使用数据库中存储的颜色，如果没有则使用默认颜色
            color = refuse_type.color or default_colors.get(refuse_type.type_name, '#1296db')
            
            types_list.append({
                'id': refuse_type.id,
                'type_name': refuse_type.type_name,
                'description': refuse_type.description,
                'icon_url': refuse_type.icon_url or '/images/default.png',
                'color': color  # 使用数据库中的颜色
            })
        
        # 返回JSON格式数据
        return jsonify({
            'success': True,
            'data': types_list
        })
    except Exception as e:
        # 错误处理
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# API接口：根据关键词搜索垃圾类别（JSON格式，供微信小程序调用）
@bp.route('/api/search')
def api_search_refuse():
    from app_package.models import RefuseCategory, RefuseType
    
    try:
        # 获取搜索关键词
        keyword = request.args.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': '搜索关键词不能为空'
            }), 400
        
        # 在refuse_categories表中搜索匹配category_name的记录
        # 使用LIKE进行模糊匹配，不区分大小写
        search_results = RefuseCategory.query.filter(
            RefuseCategory.category_name.like(f'%{keyword}%')
        ).all()
        
        if not search_results:
            return jsonify({
                'success': True,
                'data': [],
                'message': '未找到相关垃圾信息'
            })
        
        # 定义默认颜色映射作为备选
        default_colors = {
            '可回收物': '#1296db',  # 蓝色
            '有害垃圾': '#ff6b6b',  # 红色
            '厨余垃圾': '#4ecdc4',  # 绿色
            '其他垃圾': '#a8dadc',  # 灰色
        }
        
        # 收集结果
        results = []
        for category in search_results:
            # 找到对应的垃圾类型
            refuse_type = RefuseType.query.get(category.type_id)
            if refuse_type:
                # 使用数据库中存储的颜色，如果没有则使用默认颜色
                color = refuse_type.color or default_colors.get(refuse_type.type_name, '#1296db')
                
                results.append({
                    'id': category.id,
                    'category_name': category.category_name,
                    'description': category.description,
                    'sorting_guide': category.sorting_guide,
                    'type_id': category.type_id,
                    'type_name': refuse_type.type_name,
                    'type_description': refuse_type.description,
                    'icon_url': refuse_type.icon_url or '/images/default.png',
                    'color': color
                })
        
        # 返回JSON格式数据
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        # 错误处理
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500