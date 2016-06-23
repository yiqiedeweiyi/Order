__author__ = 'PC'
import sqlite3
import requests
import json
def value2JsonData(values1,values2):
    jsonDataList=[]
    jsonData=set()
    for i in values1:
        jsonDataList.append({'orderNo':i[0],'title':i[1],'contactName':i[2],'fromDate':i[3],'toDate':i[4],
                             'roomName':i[5],'roomNum':i[6],'isVisit':i[7],'isProcess':i[7]})
    for i in values2:
        jsonDataList.append({'orderNo':i[0],'title':i[1],'contactName':i[2],'fromDate':i[3],'toDate':i[4],
                             'roomName':i[5],'roomNum':i[6],'isVisit':i[7],'isProcess':i[7]})

    jsonData={'data':jsonDataList}
    return jsonData
conn = sqlite3.connect('order.db')
cursor = conn.cursor()
# 执行查询语句:
sqlStr='SELECT * FROM qunar ORDER BY orderNo DESC '
cursor.execute(sqlStr)
# cursor.execute('DROP TABLE xiecheng')
# cursor.execute('DROP TABLE qunar')
# 获得查询结果集:
values1 = cursor.fetchall()
for i in values1:
    print(i)
print('------------------------------------')
# 执行查询语句:
sqlStr='SELECT * FROM xiecheng ORDER BY orderNo DESC '
cursor.execute(sqlStr)
# cursor.execute('DROP TABLE xiecheng')
# cursor.execute('DROP TABLE qunar')
# 获得查询结果集:
values2 = cursor.fetchall()
for i in values2:
    print(i)
cursor.close()
conn.close()

jsonData=json.dumps(value2JsonData(values1,values2))
jsonData={'data':jsonData}
print(jsonData)
url1 = "http://kezhan.applinzi.com/setdata";
url2 = "http://127.0.0.1:5000/setdata";
requests.post(url2,data=jsonData)