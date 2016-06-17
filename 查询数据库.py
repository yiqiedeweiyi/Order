__author__ = 'PC'
import sqlite3
conn = sqlite3.connect('order.db')
cursor = conn.cursor()
import time
# 执行查询语句:
sqlStr='SELECT * FROM qunar ORDER BY orderNo DESC '
cursor.execute(sqlStr)
# cursor.execute('DROP TABLE xiecheng')
# cursor.execute('DROP TABLE qunar')
# 获得查询结果集:
values = cursor.fetchall()
for i in values:
    print(i)
print('------------------------------------')
# 执行查询语句:
sqlStr='SELECT * FROM xiecheng ORDER BY orderNo DESC '
cursor.execute(sqlStr)
# cursor.execute('DROP TABLE xiecheng')
# cursor.execute('DROP TABLE qunar')
# 获得查询结果集:
values = cursor.fetchall()
for i in values:
    print(i)
cursor.close()
conn.close()
