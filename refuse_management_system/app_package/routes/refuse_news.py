from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime
from app_package.models import RefuseNews, RefuseCategory

# 创建垃圾资讯管理蓝图
bp = Blueprint('refuse_news', __name__, url_prefix='/refuse-news')

# 列表所有垃圾资讯
@bp.route('/')
@login_required
def list_news():
    
    # 获取查询参数
    search_query = request.args.get('search', '')
    category_id = request.args.get('category_id', '')
    sort_by = request.args.get('sort_by', 'publish_date')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 构建查询
    query = RefuseNews.query
    
    # 搜索功能
    if search_query:
        query = query.filter(
            (RefuseNews.title.like(f'%{search_query}%')) |
            (RefuseNews.content.like(f'%{search_query}%'))
        )
    
    # 分类筛选
    if category_id and category_id in ['政策法规', '科普知识', '行业动态']:
        query = query.filter_by(category=category_id)
    
    # 排序功能
    if sort_by == 'title':
        query = query.order_by(RefuseNews.title)
    else:
        query = query.order_by(RefuseNews.publish_date.desc())
    
    # 分页查询
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    news_list = pagination.items
    
    # 获取所有分类用于筛选
    categories = RefuseCategory.query.all()
    
    # 构建查询参数，用于分页链接
    query_params = {
        'search': search_query,
        'category_id': category_id,
        'sort_by': sort_by
    }
    
    # 添加分页信息
    pagination_info = {
        'page': pagination.page,
        'pages': pagination.pages,
        'total': pagination.total,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'prev_num': pagination.prev_num if pagination.has_prev else None,
        'next_num': pagination.next_num if pagination.has_next else None,
        'page_start': (pagination.page - 1) * per_page + 1,
        'page_end': min(pagination.page * per_page, pagination.total),
        'iter_pages': pagination.iter_pages
    }
    
    return render_template(
        'refuse_news/list.html',
        news_list=pagination,
        search_query=search_query,
        categories=categories,
        selected_category=category_id,
        sort_by=sort_by,
        query_params=query_params
    )

# 添加新垃圾资讯
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_news.list_news'))
        
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        content = request.form.get('content')
        author = request.form.get('author') or current_user.username
        publish_date_str = request.form.get('publish_date')
        source = request.form.get('source')
        category = request.form.get('category')
        cover_image = request.form.get('cover_image')
        
        # 验证数据
        if not title or not content or not publish_date_str:
            flash('标题、内容和发布日期不能为空', 'danger')
            return redirect(url_for('refuse_news.add_news'))
            
        # 转换发布日期格式
        try:
            publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('发布日期格式不正确，请使用YYYY-MM-DD格式', 'danger')
            return redirect(url_for('refuse_news.add_news'))
            
        # 创建新垃圾资讯
        refuse_news = RefuseNews(
            title=title,
            subtitle=subtitle,
            content=content,
            author=author,
            publish_date=publish_date,
            source=source,
            category=category,
            cover_image=cover_image
        )
        
        try:
            db.session.add(refuse_news)
            db.session.commit()
            flash('垃圾资讯添加成功', 'success')
            return redirect(url_for('refuse_news.list_news'))
        except Exception as e:
            db.session.rollback()
            flash('垃圾资讯添加失败，请稍后再试', 'danger')
            return redirect(url_for('refuse_news.add_news'))
            
    return render_template('refuse_news/add.html')

# 编辑垃圾资讯
@bp.route('/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_news.list_news'))
        
    refuse_news = RefuseNews.query.get_or_404(news_id)
    
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        content = request.form.get('content')
        author = request.form.get('author')
        publish_date_str = request.form.get('publish_date')
        source = request.form.get('source')
        category = request.form.get('category')
        cover_image = request.form.get('cover_image')
        
        # 验证数据
        if not title or not content or not publish_date_str:
            flash('标题、内容和发布日期不能为空', 'danger')
            return redirect(url_for('refuse_news.edit_news', news_id=news_id))
            
        # 转换发布日期格式
        try:
            publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('发布日期格式不正确，请使用YYYY-MM-DD格式', 'danger')
            return redirect(url_for('refuse_news.edit_news', news_id=news_id))
            
        # 更新垃圾资讯
        refuse_news.title = title
        refuse_news.subtitle = subtitle
        refuse_news.content = content
        refuse_news.author = author
        refuse_news.publish_date = publish_date
        refuse_news.source = source
        refuse_news.category = category
        refuse_news.cover_image = cover_image
        refuse_news.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('垃圾资讯更新成功', 'success')
            return redirect(url_for('refuse_news.list_news'))
        except Exception as e:
            db.session.rollback()
            flash('垃圾资讯更新失败，请稍后再试', 'danger')
            return redirect(url_for('refuse_news.edit_news', news_id=news_id))
            
    # 格式化发布日期为YYYY-MM-DD格式
    formatted_date = refuse_news.publish_date.strftime('%Y-%m-%d') if refuse_news.publish_date else ''
    
    return render_template('refuse_news/edit.html', news=refuse_news, formatted_date=formatted_date)

# 删除垃圾资讯
@bp.route('/delete/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_news.list_news'))
        
    refuse_news = RefuseNews.query.get_or_404(news_id)
    
    try:
        db.session.delete(refuse_news)
        db.session.commit()
        flash('垃圾资讯删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash('垃圾资讯删除失败，请稍后再试', 'danger')
        
    return redirect(url_for('refuse_news.list_news'))

# 批量删除垃圾资讯
@bp.route('/batch-delete', methods=['POST'])
@login_required
def batch_delete_news():
    if not current_user.is_admin():
        flash('您没有权限执行此操作', 'danger')
        return redirect(url_for('refuse_news.list_news'))
        
    # 获取选中的垃圾资讯ID列表
    news_ids = request.form.getlist('news_ids')
    
    if not news_ids:
        flash('请至少选择一条垃圾资讯', 'warning')
        return redirect(url_for('refuse_news.list_news'))
        
    try:
        # 将字符串列表转换为整数列表
        news_ids = [int(id) for id in news_ids]
        
        # 查询所有选中的垃圾资讯
        news_to_delete = RefuseNews.query.filter(RefuseNews.id.in_(news_ids)).all()
        
        # 删除选中的垃圾资讯
        for news in news_to_delete:
            db.session.delete(news)
            
        db.session.commit()
        flash(f'成功删除了 {len(news_to_delete)} 条垃圾资讯', 'success')
    except Exception as e:
        db.session.rollback()
        flash('批量删除失败，请稍后再试', 'danger')
        
    return redirect(url_for('refuse_news.list_news'))

# 查看垃圾资讯详情
@bp.route('/detail/<int:news_id>')
@login_required
def detail_news(news_id):
    refuse_news = RefuseNews.query.get_or_404(news_id)
    
    # 增加浏览量
    refuse_news.views += 1
    try:
        db.session.commit()
    except:
        db.session.rollback()
        
    return render_template('refuse_news/detail.html', news=refuse_news)

# API接口：获取垃圾资讯列表（供小程序使用）
@bp.route('/api/list', methods=['GET'])
def api_list_news():
    # 获取查询参数
    category = request.args.get('category', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = RefuseNews.query
    
    # 分类筛选
    if category and category != 'all':
        # 直接使用传入的category参数进行筛选，确保与数据库中的值匹配
        query = query.filter_by(category=category)
    
    # 按发布日期排序
    query = query.order_by(RefuseNews.publish_date.desc())
    
    # 分页查询
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    news_list = pagination.items
    
    # 转换为JSON可序列化的格式
    result = {
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'per_page': per_page,
        'has_more': pagination.has_next,
        'news_list': [{
            'id': news.id,
            'title': news.title,
            'subtitle': news.subtitle,
            'date': news.publish_date.strftime('%Y-%m-%d'),
            'views': news.views,
            'likes': news.likes,
            'category': news.category,
            'image': news.cover_image or '/images/default.png'
        } for news in news_list]
    }
    
    return jsonify(result)

# API接口：获取垃圾资讯详情（供小程序使用）
@bp.route('/api/detail/<int:news_id>', methods=['GET'])
def api_detail_news(news_id):
    refuse_news = RefuseNews.query.get_or_404(news_id)
    
    # 增加浏览量
    refuse_news.views += 1
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    # 转换为JSON可序列化的格式
    result = {
        'id': refuse_news.id,
        'title': refuse_news.title,
        'subtitle': refuse_news.subtitle,
        'date': refuse_news.publish_date.strftime('%Y-%m-%d'),
        'author': refuse_news.author,
        'source': refuse_news.source,
        'views': refuse_news.views,
        'likes': refuse_news.likes,
        'category': refuse_news.category,
        'coverImage': refuse_news.cover_image,
        'content': refuse_news.content
    }
    
    return jsonify(result)

# API接口：点赞垃圾资讯（供小程序使用）
@bp.route('/api/like/<int:news_id>', methods=['POST'])
def api_like_news(news_id):
    refuse_news = RefuseNews.query.get_or_404(news_id)
    
    # 增加点赞数
    refuse_news.likes += 1
    try:
        db.session.commit()
        return jsonify({'success': True, 'likes': refuse_news.likes})
    except:
        db.session.rollback()
        return jsonify({'success': False, 'message': '点赞失败'}), 500