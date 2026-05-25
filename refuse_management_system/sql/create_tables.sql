-- 创建垃圾类型表
-- 垃圾类型表
CREATE TABLE IF NOT EXISTS refuse_types (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '类型ID',
    type_name VARCHAR(50) NOT NULL COMMENT '垃圾类型名称',
    description TEXT COMMENT '类型描述',
    icon_url VARCHAR(500) COMMENT '图标URL',
    color VARCHAR(7) DEFAULT '#1296db' COMMENT '类型颜色，默认蓝色',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type_name (type_name),
    UNIQUE KEY unique_type_name (type_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='垃圾类型表';

-- 垃圾分类表
CREATE TABLE IF NOT EXISTS refuse_categories (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '分类ID',
    type_id INT UNSIGNED NOT NULL COMMENT '垃圾类型ID',
    category_name VARCHAR(100) NOT NULL COMMENT '垃圾名称',
    description TEXT COMMENT '垃圾描述',
    sorting_guide TEXT COMMENT '分类指南',
    image_url VARCHAR(500) COMMENT '图片URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type_id (type_id),
    INDEX idx_category_name (category_name),
    UNIQUE KEY unique_category_type (category_name, type_id),
    FOREIGN KEY (type_id) REFERENCES refuse_types(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='垃圾分类表';

-- 垃圾资讯表
CREATE TABLE IF NOT EXISTS refuse_news (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '资讯ID',
    title VARCHAR(255) NOT NULL COMMENT '资讯标题',
    subtitle VARCHAR(255) COMMENT '副标题',
    publish_date DATE NOT NULL COMMENT '发布日期',
    author VARCHAR(100) COMMENT '作者',
    source VARCHAR(100) COMMENT '来源',
    views INT UNSIGNED DEFAULT 0 COMMENT '浏览量，非负整数',
    likes INT UNSIGNED DEFAULT 0 COMMENT '点赞数，非负整数',
    category VARCHAR(50) COMMENT '分类',
    cover_image VARCHAR(500) COMMENT '封面图片URL',
    content LONGTEXT NOT NULL COMMENT '资讯内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_title (title),
    INDEX idx_publish_date (publish_date),
    INDEX idx_category (category),
    FULLTEXT INDEX ft_title_subtitle (title, subtitle)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='垃圾资讯表';

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（哈希存储）',
    email VARCHAR(100) NOT NULL COMMENT '邮箱',
    role ENUM('admin', 'user') DEFAULT 'user' COMMENT '用户角色',
    avatar VARCHAR(500) COMMENT '头像URL',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    UNIQUE KEY unique_username (username),
    UNIQUE KEY unique_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户表';

-- 分类查询记录表（新增）
CREATE TABLE IF NOT EXISTS category_searches (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    category_id INT UNSIGNED NOT NULL COMMENT '查询的分类ID',
    user_id INT UNSIGNED COMMENT '用户ID，可为空表示匿名用户',
    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '查询时间',
    search_ip VARCHAR(45) COMMENT '查询IP地址',
    INDEX idx_category_id (category_id),
    INDEX idx_user_id (user_id),
    INDEX idx_search_time (search_time),
    FOREIGN KEY (category_id) REFERENCES refuse_categories(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='分类查询记录表';