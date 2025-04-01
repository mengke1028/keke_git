# -*- coding: utf-8 -*-
# Keke.Meng  2025/3/31 13:15
import mysql.connector
from mysql.connector import Error
import time

class MySQLDatabase:
    def __init__(self):
        self.host = '106.54.233.105'
        self.database = 'keke_test'
        self.user = 'keke'
        self.password = 'mengke1028..'
        self.connection = None
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def add_code(self, key):
        # 往数据库增加卡密
        insert_query = f"INSERT INTO activation_codes (activation_code, start_time, is_destroyed) VALUES ('{key}', NULL ,0)"
        cursor = self.connection.cursor()
        if insert_query:
            cursor.execute(insert_query)
            self.connection.commit()
            print("Query executed successfully")

    def read_query(self):
        # 查询全部的数据
        query = "SELECT * FROM activation_codes"
        if self.connection:
            cursor = self.connection.cursor()
            result = None
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Error while reading query: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('Connection to MySQL database closed')

    def update_code(self, key):
        """更新卡密状态为 1 并记录当前时间 """
        current_time = str(int(time.time()))
        update_query = "UPDATE activation_codes SET start_time = %s, is_destroyed = 1 WHERE activation_code = %s"
        values = (current_time, key)

        cursor = self.connection.cursor()
        cursor.execute(update_query, values)
        rows_affected = cursor.rowcount
        self.connection.commit()
        if rows_affected == 0:
            print(f"卡密 {key} 可能不存在")
            return False
        else:
            return True

    def query_by_activation_code(self, activation_code):
        """根据 activation_code 查询记录"""
        query = "SELECT * FROM activation_codes WHERE activation_code = %s"
        values = (activation_code,)
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, values)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"查询数据时出现错误: {e}")
        return None

    def shiyongkami(self, activation_code):
        """使用卡密 """
        data = self.query_by_activation_code(activation_code)

        if not data:
            return '卡密不存在'
        stat_time = data[0][1]
        if stat_time is None:
            # 执行修改
            try:
                self.update_code(activation_code)
                print(f'{activation_code} 状态修改成 1, 记录时间')
                return True, f'卡密还有{4}小时过期'
            except Exception as e:
                print(e)
                print(f"卡密 {activation_code} 可能不存在")
                return '卡密错误'
        else:
            low_time = int(time.time()) - int(stat_time)
            if low_time > 14400:  # 4小时试用期
                return '试用超时了'
            else:
                print(f'卡密还有{int((14400-low_time)/3600)}小时过期')
                return True, f'卡密还有{int((14400-low_time)/3600)}小时过期'


if __name__ == "__main__":

    db = MySQLDatabase()
    # 试用卡密
    activation_code = 'rbakHq4Odcyq5tJKDN7e'
    data = db.shiyongkami(activation_code)
    print(data)
    # 新增数据
    # with open('activation_codes.txt', 'r',encoding='utf-8') as pf:
    #     data = [line.strip() for line in pf.readlines()]
    #     print(data)
    # for insert_query in data:
    #
    #     try:
    #         # insert_query = '0acRraZM3rdtI9LI4RQO'
    #         db.add_code(insert_query)
    #     except Exception as e:
    #         print(f'上传失败，{insert_query}卡密可能已经存在')

    db.close_connection()
