#-*- encoding:UTF-8 -*-
from tools.CrawlerBase import *
from tools.MysqlBase import *                          
import sys
import urlparse
import json 
import time

db = MysqlBase('python')
count = 0;
crawlernew = CrawlerBase()

def extract(page):
    if page is None:
        return (None,None,None)
    
    linkpattern = re.compile(u'<span class="link_title"><a href="(.*?)">', re.S | re.U)
    links = linkpattern.findall(page)
    for i in range(len(links)):
        links[i]=u'http://blog.csdn.net'+links[i]
    return (links)

def process_article(article,link):
    title = ''
    body = ''
    dt=''
    img_urls = []
    
    titlepattern = re.compile(u'<span class="link_title"><a href="[^<]*">([^<]*?)</a></span>', re.S | re.U)
    result = titlepattern.search(article)
    if result is not None:
        title = result.group(1).strip()
        
    bodypattern = re.compile(u'<div id="article_content"[^>]*?>(.*?)</div>[^<]*?<!-- Baidu Button BEGIN -->', re.S | re.U)
    result = bodypattern.search(article)
    if result is not None:
        body = result.group(1)

    imgpattern = re.compile(u'<span class="link_postdate">(.*?)</span>', re.S | re.U | re.I)
    result = imgpattern.search(article)
    if result is not None:
        dt = result.group(1)
       
    print 'title=',title.encode('gb2312')
    global db,count,crawlernew
    
    sql=''
    count=count+1
    if count%10==0:
        db.connect()
    title = title.replace("\r", u'')
    body = body.replace("\n", u'')
    db.insert('insert ignore into blog(dt,link,title,body,tags,categories,bid) values(%s,%s,%s,%s,%s,%s,%s)',(dt,link, title, body,','.join([]),','.join([]),0));
    return 'stop'

    
if __name__ == '__main__':
    name = sys.argv[1]
    if name is not None:
        crawler = CrawlerBase()
        crawler.start(u'http://blog.csdn.net/'+name+'/article/list/%s',extract,process_article,10)
    else:
        print 'name is none'
