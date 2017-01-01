# coding : UFT-8
import requests
import random
import time
import csv
import re
import pymysql
from bs4 import BeautifulSoup
try:
    import cookielib
except:
    import http.cookiejar as cookielib

#该代码爬豆瓣电视剧如果蜗牛有爱情的影评，并存入数据库
#报文头设置
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'movie.douban.com',
    'Referer' : 'https://movie.douban.com/subject/26345137/collections',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

#豆瓣评论页面url
commentUrl = 'https://movie.douban.com/subject/26345137/collections'
doingUrl = 'https://movie.douban.com/subject/26345137/doings'
timeout = random.choice(range(60,180))

#豆瓣评分等级
gradeDic = {
    '力荐':5,
    '推荐':4,
    '还行':3,
    '较差':2,
    '很差':1
}

#爬取当页内容
def get_html(url):
    while True:
        try:
            rep = requests.get(url,headers=headers,timeout=timeout)
            print(rep)
            break
        except:
            print(url,"页面访问失败")
    return rep.text

#解析当前内容
def get_data(html):
    final = []
    bs4 = BeautifulSoup(html,"html.parser").body.find(class_='sub_ins')#找到评论区
    comment_first = bs4.find('table')#看该页是否有内容
    if comment_first is not None:
        comment_lists = bs4.find_all('table')
        nexUrl = BeautifulSoup(html, "html.parser").body.find(class_='paginator').find('span', class_='next').find('a').get('href')  # 找到下一页url

        for comment in comment_lists:
            temp = []
            info = comment.find_all('td')[1]  # 获取用户和评分信息栏
            username = [text for text in info.find('a').stripped_strings][0] # 获取用户名，去掉span！！
            if info.find('a').span is not None:
                city = info.find('a').span.get_text()  # 获取城市名字
                city = city.replace('(','').replace(')','')#去掉括号
            else:
                city = None
            data = info.find_all('p')
            time = data[0].get_text()  # 获取用户评论时间
            time = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', time)  # 正则表达式
            if data[0].find(class_=re.compile("allstar")) is not None:  # 找到评分栏
                temp.append(username)  # 添加用户信息
                temp.append(city)
                temp.append(time.group())
                grade = data[0].find(class_=re.compile("allstar")).get('title')  # 获取用户评分
                temp.append(grade)
                temp.append(gradeDic[grade])  # 将评分转为5分制
            else:
                print("没有找到评分")
                continue
            if len(data) > 1:  # 如果用户评论不为空
                comment = data[1].get_text()  # 获取用户评论
                temp.append(comment)
            else:
                #print("用户未评论")
                temp.append("")  # 留空
            final.append(temp)
        return final,nexUrl
    else:
        print("已到最后一页")
        nexUrl = None
        return final,nexUrl

#翻页
def turn_page(url):
    count = 0
    currentUrl = url
    while currentUrl is not None:#当还有下一页时
        print(currentUrl)
        html = get_html(currentUrl)
        data,nextUrl = get_data(html)
        #write_data(data,'douban.csv')
        databases(data)
        currentUrl = nextUrl
        count = count + 1
        print(count)
        time.sleep(random.choice(range(1, 5)))

#将内容存入excel
def write_data(datas, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(datas)

#连接数据库
def databases(datas=None):
    db = pymysql.connect("localhost","root","zjh418","douban",charset='utf8mb4')
    #db = pymysql.connect("localhost","root","zjh418","douban",charset='utf8mb4')# 打开数据库连接
    # db.set_charset('utf8')
    cursor = db.cursor()# 使用 cursor() 方法创建一个游标对象 cursor
    for data in datas:
        username = data[0]
        city = data[1]
        time = data[2]
        star = data[3]
        grade = data[4]
        comment = data[5]
        print(data)
        # SQL 插入语句
        sql = "INSERT INTO comment_collections(username, \
            city,comment_time, star, grade,comment) \
            VALUES ('%s', '%s', '%s','%s', '%d','%s' )" % \
            (username, city,time,star, grade,comment)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            print("出错")
            db.rollback()
    # 关闭数据库连接
    cursor.close()#关闭游标
    db.close()

if __name__ == '__main__':
    turn_page(doingUrl)






