__author__ = 'PC'
import time
s='1465056000000'

def localTime(s):
    s=s[:len(s)-3]
    ltime=time.localtime(int(s))
    timeStr=time.strftime("%Y-%m-%d", ltime)
    return timeStr
print(localTime(s))

