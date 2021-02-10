# 抓取百度新闻网页实时信息
import urllib.request
from bs4 import BeautifulSoup 
import datetime
import time

def deleteSame(allurl): #网页排重，去掉重复数据
    datatemp = dict()
    for url in allurl:
        data = url.split('\t')
        name = data[0]
        url = data[1]
        datatemp[name] = url #用字典去除相同的链接
    allurl = []
    datatempkeys = list(datatemp.keys())
    for name in datatempkeys:
        allurl.append(name + '\t' + datatemp[name])
    return allurl



def getallurl(url): # 获取页面中所有的url
    allurl = []
    herders={ # 请求头
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like GeCKO) Chrome/45.0.2454.85 Safari/537.36 115Broswer/6.0.3',
        'Connection':'keep-alive'}
    req=urllib.request.Request(url,headers=herders)
    response=urllib.request.urlopen(req)
    html=response.read().decode('utf8')
    bsObj = BeautifulSoup(html,'html.parser')

    num = bsObj.find_all('i', class_ = 'dot') #计算热点新闻的长度
    length = len(num)
    if length > 0:   #如果有热点信息
        for i in range(length):
            hot_tags = bsObj.find_all("li", class_= 'hdline' + str(i))
            name = hot_tags[0].select('a')[0].text  # 热点新闻的词条信息
            url = hot_tags[0].select('a' )[0].attrs['href'] # 热点新闻的链接
            allurl.append('词条：' + name + '\t链接：' + url + '\n')
    
    all_tags = bsObj.find_all("a")
    for tags in all_tags: 
        url = str(tags.get("href"));
        name = str(tags.text)
        lenthname = len(name);
        if (((url.find('id=') > 0 or url.find('wd=') > 0 or url.find('.htm') > 0 or url.find('.shtml') > 0 or url.find('.html') > 0) and lenthname > 5)):
                allurl.append('词条：' + name + '\t链接：' + url + '\n')
    lenurl = len(allurl)
    allurl = allurl[0 : lenurl-1]
    allurl = deleteSame(allurl)
    return allurl

def searchKeyWord(keyword, allurl): #基于关键词的网页爬取
    newdata = []
    for data in allurl:
        if data.find(keyword) > 0: # 找到关键词对应的词条
            newdata.append(data)
    if len(newdata) > 0:
        print('找到对应的词条信息')
        return newdata
    else:
        newdata.append('没有找到对应的词条信息')
        print('没有找到对应的词条信息')
        return newdata

def structSave(allurl): # 结构化存储
    curr_time = datetime.datetime.now() # 获取当前日期
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    lenurl = len(allurl)
    for i in range(lenurl):
        allurl[i] = time_str + ': ' + allurl[i]
    return allurl

def getmenu(url): # 实现多级爬取
    allurl = []
    herders={ # 请求头
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like GeCKO) Chrome/45.0.2454.85 Safari/537.36 115Broswer/6.0.3',
        'Connection':'keep-alive'}
    req=urllib.request.Request(url,headers=herders)
    response=urllib.request.urlopen(req)
    html=response.read().decode('utf8')
    bsObj = BeautifulSoup(html,'html.parser')
    all_tags = bsObj.find_all("a")
    for tags in all_tags: 
        url = str(tags.get("href"));
        name = str(tags.text)
        lenthurl = len(url);
        if (lenthurl < 10 and lenthurl > 3):
                allurl.append('词条：' + name + '\t链接：' + url + '\n')
    lenth = len(allurl) 
    finaldata = allurl[0:lenth-1]
    finaldata = deleteSame(finaldata)
    return finaldata

def getTitle(url):
    herders={ # 请求头
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like GeCKO) Chrome/45.0.2454.85 Safari/537.36 115Broswer/6.0.3',
        'Connection':'keep-alive'}
    req=urllib.request.Request(url,headers=herders)
    response=urllib.request.urlopen(req)
    html=response.read().decode('utf8')
    bsObj = BeautifulSoup(html,'html.parser')
    print(bsObj.head.title)
    print('多级网页爬取成功!')


#多层网页爬取，menu为菜单选项栏目，keywords为关键字
#menu为国内，国际，军事等
def geteverylayers(url, menu, keywords):
    menudata = getmenu(url); # 获取菜单信息
    newpage = searchKeyWord(menu, menudata) # 找到对应的菜单
    newurl = newpage[0].split('\t')[1][4:-1]
    newurl = url + newurl
    newdata = getallurl(newurl) # 第二层网页爬取

    newpage2 = searchKeyWord(keywords, newdata)
    newurl2 = newpage2[0].split('\t')[1][3:-1]
    getTitle(newurl2)
    

if __name__ == '__main__':
    # start = time.time()
    url='http://news.baidu.com/'
    curr_time = datetime.datetime.now() # 获取当前日期
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
    while True:
        urldata = getallurl(url)
        # urldata = searchKeyWord('北京理工大学', urldata) #关键词爬取
        
        urldata = structSave(urldata)
        length = len(urldata)
        with open('newsdata.txt', 'w') as f:
            f.write('百度新闻:\n')
            for i in range(length):
                f.write(urldata[i])
        print(time_str + ': 百度新闻爬取成功!')
        # end = time.time()
        # print(end - start)
        time.sleep(1) # 每隔一秒更新一次数据
    # geteverylayers(url,'国内', '中央') ## 多级爬取