
# coding=utf-8
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import xmnlp
import re
import random


def get_cookie():
    # 模拟登录QQ空间
    chrome_options = Options()
    #chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path='E:\\chromedriver\\chromedriver.exe', chrome_options=chrome_options)
    driver.get('https://qzone.qq.com/')

    time.sleep(10)#扫码登录
    # driver.find_element_by_id('login_button').click()

    with open('cookies.txt', 'w+') as f:  # 这里是将得到的cookie进行保存，这样就不用每次启动程序都要登录
        for cookie in driver.get_cookies():
            f.write(cookie['name'] + '==' + cookie['value'] + '\n')
    f.close()


def login():
    session = requests.session()  # 设置全局变量
    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
    headers = {
               'Referer': 'https://qzone.qq.com/',
               'Host': 'user.qzone.qq.com'}
    headers['User-Agent'] = random.choice(user_agent_list)

    
    with open('cookies.txt', 'r') as f:  # 从文本中获取到cookies并且变成可使用的cookies的格式
        ans = f.readlines()
    cookies = {}
    for an in ans:
        an = an.replace('\n', '')
        a = an.split('==')
        cookies[a[0]] = a[1]
    cookies['_qz_referrer'] = 'i.qq.com'
    requests.utils.add_dict_to_cookiejar(session.cookies, cookies)  # 这里就是将cookie和session绑定在一起

    r = session.get('https://user.qzone.qq.com/1357320753/infocenter', headers=headers,verify=False,timeout=5)  #
    if not re.findall('QQ空间-分享生活，留住感动', r.text):
    # 判断是否有这个，来判断是否登录成功
        return r
    else:
        return False
def get_data():

    html = login()
    if(html == False):
        get_cookie()
        html=login()
    else:
        soup = BeautifulSoup(html.content, 'lxml')

        friends = soup.findAll(attrs={'class': 'f-name q_namecard'})

        msgs = soup.findAll(attrs={'class': 'f-info'})
        with open('data.csv', 'a+',encoding='utf-8') as fo:
            for i in range(len(friends) - 1):
                num = str(friends[i].attrs['href'])
                doc = msgs[i].text
                score = xmnlp.sentiment(doc)
                print(doc)
                print('Score: ', score)
                res = ""
                if score > 0.49 :
                    res = '积极'
                else:
                    res = '消极'

                print("%s,%s,%s,%d,%s"%(friends[i].text,num.split('/')[-1],doc,score,res))
                fo.writelines("%s,%s,%s,%s,%s\n"%(friends[i].text,num.split('/')[-1],doc,str(score),res))

            fo.close()
if __name__ == '__main__':
    get_data()



