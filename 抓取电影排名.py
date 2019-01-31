# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 18:59:10 2019

@author: lenovo
"""
#请求库：requests 解析工具：正则表达式
import requests
import re
import json
import time

def get_one_page(url):
    headers={
        'User-Agent':'ozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E5216a QQ/7.5.5.426 V1_IPH_SQ_7.5.5_1_APP_A Pixel/1080 Core/UIWebView Device/Apple(iPhone 8Plus) NetType/WIFI QBWebViewType/1'
        }
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text
    return None

    
def parse_one_page(html):
    pattern=re.compile('<li>.*?<em\sclass.*?>(.*?)</em>.*?<img.*? src="(.*?)".*?title">(.*?)<.*?<p class="">(.*?)</p>.*?rating_num.*?>(.*?)<.*?<span>(.*?)</span>.*?.*?inq">(.*?)<.*?</li>',re.S)
    items=re.findall(pattern,html)
    #列表形成字典
    for item in items:
        
        print(item[3])
    for item in items:
        yield{'index':item[0],
              'image':item[1],
              'title':item[2],#.strip(),
              'actor':item[3],
              'score':item[4],#strip()[5:],
              'people_num':item[5],
              'evaluate':item[6]
                }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        print(json.dumps(content,ensure_ascii=False))
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(start):
    url='https://movie.douban.com/top250?start='+str(start)+'&filter='
    html=get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        
if __name__=='__main__':
    for i in range(10):
        start=i*25
        main(start)
        time.sleep(1)
