__author__ = 'PC'
from selenium import webdriver
import time,datetime
import requests,json
import sqlite3
heads={
    'Host':'m.ebooking.ctrip.com',
    'Connection':'keep-alive',
    'Content-Length':'126',
    'Accept':'application/json',
    'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8;',
    'Origin':'http://m.ebooking.ctrip.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'X-Requested-With':'XMLHttpRequest',
    'Referer':'http://m.ebooking.ctrip.com/Hotel-Supplier-EBookingAPP/Orders/OrderList.aspx?tab=2',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-us,en;q=0.8',
    'Cookie':''
}
def loginSelenium():
    # 使用火狐模拟登陆
    cookieStr=''
    firefoxProfile=webdriver.FirefoxProfile()
    # 设置useragent
    firefoxProfile.set_preference('general.useragent.override','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat')
    driver = webdriver.Firefox(firefoxProfile)
    driver.get("http://m.ebooking.ctrip.com/Hotel-Supplier-EBookingAPP/Home/Login.aspx")
    driver.find_element_by_id("account").send_keys("叶漫芬")
    driver.find_element_by_id("password").send_keys("abc1234")
    driver.find_element_by_id("login").click()
    for i in range(len(driver.get_cookies())):
        cookieStr=cookieStr+driver.get_cookies()[i]['name']+'='+driver.get_cookies()[i]['value']+';'
    driver.quit()
    print(cookieStr[:len(cookieStr)-1])
    return cookieStr[:len(cookieStr)-1]
def proData(allOrderSet,jsonData):
    for i in range(len(jsonData)):
        allOrderSet.add((int(jsonData[i]['OrderID']),'wwwxiecheng',jsonData[i]['ShortClientName'],jsonData[i]['Arrival'],jsonData[i]['Departure']
            ,jsonData[i]['RoomName'],jsonData[i]['Quantity']))
def saveInSqllite(allOrderSet):
    # 连接到SQLite数据库,数据库文件是test.db,如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('order.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表:
    try:
        cursor.execute('create table xiecheng (orderNo int primary key,title varchar(20), contactName varchar(20),'
                   'fromDate varchar(20),toDate varchar(20),roomName varchar(20),roomNum varchar(20),isVisit varchar(20),isProcess varchar(20))')
    except:print('表已存在！')
    cursor.execute('select * from xiecheng')
    # 获得查询结果集:
    values = cursor.fetchall()
    for i in allOrderSet:
        isIn=False
        for j in values:
            if(i[0] in j):
                isIn=True
        if(not isIn):
            sqlStr='insert into xiecheng (orderNo,title,contactName,fromDate,toDate,roomName,roomNum,isVisit,isProcess) values ('+str(i[0])\
                   +',\''+str(i[1])+'\',\''+str(i[2])+'\',\''+str(i[3])+'\',\''+str(i[4])+'\',\''+str(i[5])+'\',\''+str(i[6])+'\',\''+'1'+'\',\''+'1'+'\')'
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
heads['Cookie']=loginSelenium()
url='http://m.ebooking.ctrip.com/Hotel-Supplier-EBookingAPP/Ajax/Orders/OrderQuery.ashx'
file=open('log.txt','a')
networkError=0
jsonError=0
jsonPoageCountError=0
while(True):
    pageIndex=1
    allOrderSet=set()
    print(datetime.datetime.now())
    file.write(str(datetime.datetime.now())+'\n')
    while(True):
        postData={
            'Method':'GetAllOrderList',
            'PageIndex':pageIndex,
            'PerPageCount':'20',
            'SplitFormid':'',
            'FormStatus':'',
            'CheckInStarDateTime':'',
            'PullType':'undefined',
            'DayBefore':''
        }

        try:
            r=requests.post(url,data=postData,headers=heads)
            try:
                jsonData=json.loads(r.text)
            except:
                jsonError+=1
                print('json解析失败')
                file.write('json解析失败'+'\n')
                if(jsonError>4):
                    print('json解析失败，重新启用火狐登陆')
                    file.write('json解析失败，重新启用火狐登陆'+'\n')
                    try:
                        heads['Cookie']=loginSelenium()
                    except:print('启动浏览器失败')
                    jsonError=0
            file.write(str(jsonData)+'\n')
            try:
                jsonDataList=jsonData['Data']['OrderList']
                proData(allOrderSet,jsonDataList)
                saveInSqllite(allOrderSet)

            except TypeError :
                print('order解析失败')

            try:
                if(jsonData['Data']['PageCount']==jsonData['Data']['PageIndex']):
                    break
                    print('没有更多数据！')
            except:
                jsonPoageCountError+=1
                print('PageCount解析失败')
                file.write('PageCount解析失败'+'\n')
                if(jsonPoageCountError>4):
                    print('PageCount解析失败，重新启用火狐登陆')
                    file.write('PageCount解析失败，重新启用火狐登陆'+'\n')
                    try:
                        heads['Cookie']=loginSelenium()
                    except:print('启动浏览器失败')
                    jsonPoageCountError=0
        except networkError :
            networkError+=1
            print('网络连接有误')
            file.write('网络连接有误'+'\n')
            if(networkError>4):
                print('网络连接有误，重新启用火狐登陆')
                file.write('网络连接有误，重新启用火狐登陆'+'\n')
                try:
                    heads['Cookie']=loginSelenium()
                except:print('启动浏览器失败')
                networkError=0
        file.flush()
        pageIndex+=1
        time.sleep(10)
    time.sleep(60)
