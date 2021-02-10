# 抓取微博热搜词条信息
import urllib.request
from bs4 import BeautifulSoup 
import datetime
import time

def getdata(url):
    newsdata = []
    # 请求头
    herders={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like GeCKO) Chrome/45.0.2454.85 Safari/537.36 115Broswer/6.0.3',
        'Connection':'keep-alive'}
    req=urllib.request.Request(url,headers=herders)
    response=urllib.request.urlopen(req)
    html=response.read().decode('utf8')
    bsObj = BeautifulSoup(html,'html.parser')
    curr_time = datetime.datetime.now() # 获取当前日期
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    all_tags = bsObj.find_all("a")
    url2 = 'https://s.weibo.com'
    with open('weiBoSearch.txt', 'w') as f: 
        f.write(str(bsObj.head.title)[7:-8] + '\n')
        for tags in all_tags:
            url = str(tags.get("href"))
            name = str(tags.text)
            lenurl = len(url)
            lename = len(name)
            if url.find('q=') > 0 and name != '意见反馈':
                newurl = url2 + url
                f.write(time_str + ':  词条：' + name + '    链接：' + newurl + '\n')
    print(time_str + ' ' + str(bsObj.head.title)[7:-8]+ '爬取成功！\n')

if __name__ == '__main__':
    url='https://s.weibo.com/top/summary'
    while True:
        getdata(url)
        time.sleep(1)  
