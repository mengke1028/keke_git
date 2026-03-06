# -*- coding: utf-8 -*-
# TCN01475  2026/3/6 8:53
# server.py - 后端API服务
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

# 数据库配置（仅在服务器端保存）
DB_CONFIG = {
    'host': '43.136.80.203',
    'database': 'keke_test',
    'user': 'keke',
    'password': 'mengke1028..'
}


def create_db_connection():
    """创建数据库连接"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"数据库连接错误: {e}")
    return connection


def verify_activation_code(code):
    """验证卡密的核心逻辑（和原代码一致）"""
    connection = create_db_connection()
    if not connection:
        return {"status": "error", "message": "数据库连接失败"}

    try:
        # 1. 查询卡密
        cursor = connection.cursor()
        query = "SELECT start_time, is_destroyed FROM activation_codes WHERE activation_code = %s"
        cursor.execute(query, (code,))
        result = cursor.fetchone()

        if not result:
            return {"status": "fail", "message": "卡密不存在"}

        start_time = result[0]
        is_destroyed = result[1]

        # 2. 验证卡密状态
        if start_time is None:
            # 首次使用，更新状态和时间
            current_time = int(time.time())
            update_query = """
                UPDATE activation_codes 
                SET start_time = %s, is_destroyed = 1 
                WHERE activation_code = %s
            """
            cursor.execute(update_query, (current_time, code))
            connection.commit()
            return {"status": "success", "message": "卡密还有4小时过期"}

        else:
            # 非首次使用，检查是否超时
            elapsed_time = int(time.time()) - int(start_time)
            remaining_hours = int((14400 - elapsed_time) / 3600)

            if elapsed_time > 14400:
                return {"status": "fail", "message": "试用超时了"}
            else:
                return {"status": "success", "message": f"卡密还有{remaining_hours}小时过期"}

    except Error as e:
        print(f"数据库操作错误: {e}")
        return {"status": "error", "message": "服务器内部错误"}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/verify_code', methods=['POST'])
def verify_code_api():
    """卡密验证API接口"""
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({"status": "fail", "message": "请提供卡密参数"}), 400

    code = data['code'].strip()
    result = verify_activation_code(code)
    return jsonify(result)


if __name__ == '__main__':
    # 运行Flask服务（生产环境建议用Gunicorn+Nginx）
    app.run(host='0.0.0.0', port=5000, debug=True)