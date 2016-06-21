__author__ = 'PC'
# 不使用文件存储，使用sqllite
import requests
import json
import time
import sqlite3
heads={
    'Host':'ebooking.qunar.com',
    'Connection':'keep-alive',
    'Accept':'application/json',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/45.0.2454.95 Mobile Safari/537.36 ebaiphone/60001009',
    'Referer':'http://ebooking.qunar.com/touch/app/order/manage.htm?showSelect=true',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,en-US;q=0.8',
    'Cookie':'_v=5yRwPMVbpfK720aL_fyEUpWsWO51kxBjTodfHgzHSFJIwfFZbsKtlpMsUd0gzcwzmXTjU02N-J9K__C18STjSXlYSfXbddQOTfUH5qEfvTFrwZhlZxSys9pG5eoWCwbTchtaq-xtJjayCuGHnqVDjAKCzeLLETXv3JdbAi5F57PP; _t=24407965; _q=U.qunarppb_1406908251; _gid=1f0fe34d-154f9afa9f8-931f4ac658af18fecdadd8915186b8f1',
}
def localTime(s):
    s=s[:len(s)-3]
    ltime=time.localtime(int(s))
    timeStr=time.strftime("%Y-%m-%d", ltime)
    return timeStr
def proData(allOrderSet,jsonData):
    for i in range(len(jsonData)):
        allOrderSet.add((int(jsonData[i]['orderNo']),'wwwqunar',jsonData[i]['customerNames'],jsonData[i]['fromDate'],jsonData[i]['toDate']
            ,jsonData[i]['roomName'],jsonData[i]['roomNum']))
def saveInSqllite(allOrderSet):
    # 连接到SQLite数据库,数据库文件是test.db,如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('order.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表:
    try:
        cursor.execute('create table qunar (orderNo int primary key,title varchar(20), contactName varchar(20),'
                   'fromDate varchar(20),toDate varchar(20),roomName varchar(20),roomNum varchar(20),isVisit varchar(20))')
    except:print('表已存在！')
    cursor.execute('select * from qunar')
    # 获得查询结果集:
    values = cursor.fetchall()
    for i in allOrderSet:
        isIn=False
        for j in values:
            if(i[0] in j):
                isIn=True
        if(not isIn):
            sqlStr='insert into qunar (orderNo,title,contactName,fromDate,toDate,roomName,roomNum,isVisit) values ('+str(i[0])\
                   +',\''+str(i[1])+'\',\''+str(i[2])+'\',\''+localTime(str(i[3]))+'\',\''+localTime(str(i[4]))+'\',\''+str(i[5])+'\',\''+str(i[6])+'\',\''+'1'+'\')'
            print(sqlStr)
            cursor.execute(sqlStr)
            print('添加成功:'+str(i))
        else:
            print('已存在数据库:'+str(i))
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()
while(True):
    indexPage=1
    allOrderSet=set()
    jsonData={'data':{'list':[]}}
    while(True):
        url='http://ebooking.qunar.com/ebooking/app/api?_pid=1109&pageSize=10&curPage='+str(indexPage)+'&_a=EB_APP_TOUCH&_=1464572895997'
        postData={
          '':''
        }
        try:
            r=requests.post(url,data=postData,headers=heads)
        except:
            r=None
            print('网络连接失败')
        try:
            jsonData=json.loads(r.text)
        except:
            print('数据解析失败')
        jsonDataList=jsonData['data']['list']
        if(len(jsonDataList)>0):
            proData(allOrderSet,jsonDataList)
            saveInSqllite(allOrderSet)
            indexPage+=1
        else:
            print('没有更多数据！')
            break
        time.sleep(10)
    time.sleep(60*1)
    