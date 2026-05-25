# -*- coding: utf-8 -*-
"""测试MySQL连接的脚本"""

import pymysql

def test_mysql_connection():
    # 尝试不同的连接配置进行测试
    configs = [
        # 配置1: root用户，空密码
        {'host': 'localhost', 'user': 'root', 'password': '', 'charset': 'utf8mb4'},
        # 配置2: root用户，密码为'password'
        {'host': 'localhost', 'user': 'root', 'password': '123456', 'charset': 'utf8mb4'},
        # 配置3: root用户，密码为'root'
        {'host': 'localhost', 'user': 'root', 'password': 'root', 'charset': 'utf8mb4'},
    ]
    
    for i, config in enumerate(configs):
        try:
            print(f"测试配置 {i+1}: 用户={config['user']}, 密码={'******' if config['password'] else '空'}")
            conn = pymysql.connect(**config)
            print(f"✓ 配置 {i+1} 连接成功！")
            conn.close()
            return config  # 返回成功的配置
        except Exception as e:
            print(f"✗ 配置 {i+1} 连接失败: {str(e)}")
    
    print("\n所有配置都连接失败。请手动检查MySQL服务器配置。")
    print("可能的解决方案:")
    print("1. 确保MySQL服务器已启动")
    print("2. 检查root用户的密码设置")
    print("3. 修改脚本中的配置，使用正确的用户名和密码")
    return None

if __name__ == '__main__':
    print("开始测试MySQL连接...")
    success_config = test_mysql_connection()
    if success_config:
        print("\n成功连接MySQL服务器！")
        print("请使用以下配置更新您的项目设置：")
        print(f"- 主机: {success_config['host']}")
        print(f"- 用户: {success_config['user']}")
        print(f"- 密码: {'******' if success_config['password'] else '空'}")
        print(f"- 数据库URL示例: mysql+pymysql://{success_config['user']}{':'+success_config['password'] if success_config['password'] else ''}@{success_config['host']}/refuse_management")