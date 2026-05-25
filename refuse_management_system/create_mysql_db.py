# -*- coding: utf-8 -*-
"""创建MySQL数据库的脚本"""

import pymysql

# 数据库连接配置
# 默认配置为root用户，密码为空，localhost地址
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 如果MySQL服务器有密码，请修改这里
    'charset': 'utf8mb4'
}

def create_database():
    try:
        # 连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # 创建数据库
        database_name = 'refuse_management'
        create_db_sql = f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cursor.execute(create_db_sql)
        
        print(f"数据库 '{database_name}' 已成功创建或已存在！")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"创建数据库失败: {str(e)}")
        print("请检查MySQL服务器是否运行，以及连接信息是否正确。")
        print("注意：")
        print("1. 确保MySQL服务器已启动")
        print("2. 确保root用户有权限创建数据库")
        print("3. 如果root用户有密码，请修改此脚本中的password配置")
        return False

if __name__ == '__main__':
    create_database()