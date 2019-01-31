# Webspider_exp2
豆瓣网Top250电影数据爬取（requests库、正则表达式解析）
### 爬取豆瓣Top250电影的评分、海报、影评等数据！
 &ensp;  本项目是爬虫中最基础的，最简单的一例；
后面会有利用爬虫框架来完成更高级、自动化的爬虫程序。
&ensp; 此项目过程是运用requests请求库来获取html，再用正则表达式来解析从中获取所需数据。


话不多说，直接上代码，盘！  （具体代码解释在代码旁边）
##### 1.加载包，requests请求库，re是正则表达式的包，json是后面来把字典序列化的包；
```python

#请求库：requests    解析工具：正则表达式
import requests
import re
import json
import time
```
##### 2.用requests库通过url获取响应，得到html文本。
```Python
def get_one_page(url):
    #头部的定义，自己在网页中可以获取（网页右击检查，network中的header）
    headers={
        'User-Agent':'ozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E5216a QQ/7.5.5.426 V1_IPH_SQ_7.5.5_1_APP_A Pixel/1080 Core/UIWebView Device/Apple(iPhone 8Plus) NetType/WIFI QBWebViewType/1'
        }
    response=requests.get(url,headers=headers)
    if response.status_code==200:  #只有status_code为200时才表示响应正确
        return response.text
    return None
```
##### 3.用正则表达式从html中匹配出想要数据
```Python
def parse_one_page(html):
    #re.compile是把正则化字符串对象化，方便复用。
    pattern=re.compile('<li>.*?<em\sclass.*?>(.*?)</em>.*?<img.*? src="(.*?)".*?title">(.*?)<.*?<p class="">(.*?)</p>.*?rating_num.*?>(.*?)<.*?<span>(.*?)</span>.*?.*?inq">(.*?)<.*?</li>',re.S)
    items=re.findall(pattern,html)
    #列表形成字典（通过findall获取的数据是一条条记录，形成一个列表）

    for item in items:
        yield{'index':item[0],  #电影排名
              'image':item[1],  #电影海报
              'title':item[2],  #电影名称
              'actor':item[3],  #电影导演，主演
              'score':item[4],  #评分
              'people_num':item[5],  #多少人评价
              'evaluate':item[6]     #影评
                }
```
##### 4.把获得的数据存入到txt文件当中去
```Python

def write_to_file(content):
    #创建或打开result.txt以追加的读写方式写入数据
    with open('result.txt','a',encoding='utf-8') as f:
        print(json.dumps(content,ensure_ascii=False))  #json.dumps()用于把字典序列化，方便写入txt文件
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
```
##### 5.通过改变url中start的值来实现换页，进行下一页的切换。
```Python
def main(start):
    #更换url中的start值来切换页面，具体更换的数值要更具实际情况而变
    url='https://movie.douban.com/top250?start='+str(start)+'&filter='
    html=get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__=='__main__':
    for i in range(10):
        start=i*25
        main(start)
        time.sleep(1)#防止请求过快被网页检测出来，休眠1秒

```
 &ensp; 本文所有代码复制可以直接运行欧！我的博客：https://home.cnblogs.com/u/xubin97/ 更多内容~
