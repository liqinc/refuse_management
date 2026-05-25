from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime

# 创建垃圾分类管理蓝图
bp = Blueprint('refuse_category', __name__, url_prefix='/refuse_categories')

# 列表所有垃圾分类
@bp.route('/')
@login_required
def list_categories():
    from app_package.models import RefuseCategory, RefuseType
    
    # 获取所有垃圾类型（用于筛选下拉菜单）
    refuse_types = RefuseType.query.all()
    
    # 获取搜索和筛选参数
    search_query = request.args.get('search', '')
    type_id = request.args.get('type_id')
    sort_by = request.args.get('sort_by', 'created_at')
    
    # 构建查询
    query = RefuseCategory.query
    
    # 应用搜索筛选
    if search_query:
        query = query.filter(RefuseCategory.category_name.like(f'%{search_query}%'))
    
    # 应用类型筛选
    if type_id:
        query = query.filter_by(type_id=type_id)
    
    # 应用排序
    if sort_by == 'name':
        query = query.order_by(RefuseCategory.category_name)
    else:
        query = query.order_by(RefuseCategory.created_at.desc())
    
    # 获取所有符合条件的分类
    categories = query.all()
    
    return render_template('refuse_category/list.html', 
                          categories=categories, 
                          refuse_types=refuse_types, 
                          search_query=search_query, 
                          selected_type=type_id, 
                          sort_by=sort_by)

# 添加新垃圾分类
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    from app_package.models import RefuseCategory, RefuseType
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_category.list_categories'))
        
    # 获取所有垃圾类型
    refuse_types = RefuseType.query.all()
    
    if request.method == 'POST':
        # 获取表单数据
        type_id = request.form.get('type_id')
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        sorting_guide = request.form.get('sorting_guide')
        image_url = request.form.get('image_url')
        
        # 验证数据
        if RefuseCategory.query.filter_by(category_name=category_name, type_id=type_id).first():
            flash('该垃圾类型下已存在同名垃圾', 'danger')
            return redirect(url_for('refuse_category.add_category'))
            
        # 创建新垃圾分类
        refuse_category = RefuseCategory(
            type_id=type_id,
            category_name=category_name,
            description=description,
            sorting_guide=sorting_guide,
            image_url=image_url
        )
        
        try:
            db.session.add(refuse_category)
            db.session.commit()
            flash('垃圾分类添加成功', 'success')
            return redirect(url_for('refuse_category.list_categories'))
        except Exception as e:
            db.session.rollback()
            flash('垃圾分类添加失败，请稍后再试', 'danger')
            return redirect(url_for('refuse_category.add_category'))
            
    return render_template('refuse_category/add.html', refuse_types=refuse_types)

# 编辑垃圾分类
@bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_category.list_categories'))
        
    refuse_category = RefuseCategory.query.get_or_404(category_id)
    refuse_types = RefuseType.query.all()
    
    if request.method == 'POST':
        # 获取表单数据
        type_id = request.form.get('type_id')
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        sorting_guide = request.form.get('sorting_guide')
        image_url = request.form.get('image_url')
        
        # 验证数据
        existing_category = RefuseCategory.query.filter_by(category_name=category_name, type_id=type_id).first()
        if existing_category and existing_category.id != category_id:
            flash('该垃圾类型下已存在同名垃圾', 'danger')
            return redirect(url_for('refuse_category.edit_category', category_id=category_id))
            
        # 更新垃圾分类
        refuse_category.type_id = type_id
        refuse_category.category_name = category_name
        refuse_category.description = description
        refuse_category.sorting_guide = sorting_guide
        refuse_category.image_url = image_url
        refuse_category.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('垃圾分类更新成功', 'success')
            return redirect(url_for('refuse_category.list_categories'))
        except Exception as e:
            db.session.rollback()
            flash('垃圾分类更新失败，请稍后再试', 'danger')
            return redirect(url_for('refuse_category.edit_category', category_id=category_id))
            
    return render_template('refuse_category/edit.html', category=refuse_category, refuse_types=refuse_types)

# 删除垃圾分类
@bp.route('/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    from app_package.models import RefuseCategory
    
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_category.list_categories'))
        
    refuse_category = RefuseCategory.query.get_or_404(category_id)
    
    try:
        db.session.delete(refuse_category)
        db.session.commit()
        flash('垃圾分类删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash('垃圾分类删除失败，请稍后再试', 'danger')
        
    return redirect(url_for('refuse_category.list_categories'))

# 查看垃圾分类详情
@bp.route('/detail/<int:category_id>')
@login_required
def detail_category(category_id):
    refuse_category = RefuseCategory.query.get_or_404(category_id)
    return render_template('refuse_category/detail.html', category=refuse_category)

# 批量删除垃圾分类
@bp.route('/batch-delete', methods=['POST'])
@login_required
def batch_delete_categories():
    from app_package.models import RefuseCategory
    
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_category.list_categories'))
        
    # 获取选中的分类ID列表
    category_ids = request.form.getlist('category_ids')
    
    print(f"\n=== 批量删除调试信息 ===")
    print(f"接收到的category_ids: {category_ids}")
    
    if not category_ids:
        flash('请至少选择一个垃圾分类进行删除', 'warning')
        print("警告: 未接收到任何分类ID")
        return redirect(url_for('refuse_category.list_categories'))
        
    try:
        # 查询并删除选中的垃圾分类
        deleted_count = 0
        print(f"开始删除 {len(category_ids)} 个分类...")
        
        for category_id in category_ids:
            print(f"尝试删除分类ID: {category_id}")
            refuse_category = RefuseCategory.query.get_or_404(category_id)
            print(f"找到分类: {refuse_category.category_name}, ID: {refuse_category.id}")
            db.session.delete(refuse_category)
            deleted_count += 1
            print(f"已标记删除，当前已标记: {deleted_count}")
        
        db.session.commit()
        print(f"✅ 数据库提交成功，共删除 {deleted_count} 个分类")
        flash(f'成功删除 {deleted_count} 个垃圾分类', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"❌ 删除过程中出错: {str(e)}")
        flash('批量删除失败，请稍后再试', 'danger')
        
    return redirect(url_for('refuse_category.list_categories'))