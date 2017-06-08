#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *
from tools.CrawlerBase import *
import subprocess
import time 
if __name__ == '__main__':    
    crawler = CrawlerBase()
    db = MysqlBase('python')
    for i in range(0):
        url = u'https://www.cnblogs.com/sitehome/p/'+str(i+1)        
        page = crawler.get_html(url)
        linkpattern = re.compile(u'<a class="titlelnk" href="http://www.cnblogs.com/(.*?)/p/.*?" target="_blank">', re.S | re.U)
        links = linkpattern.findall(page)    
        for link in links:
            print link
            db.insert('insert ignore into bloglist(type,name) values(%s,%s)',('cnblog',link));   
        #mysql.insert('insert into bloglist(type,name) values(%s,%s)',('cnblog',_name));   
    
    #get expert
    for i in range(57):
        url = u'http://www.cnblogs.com/mvc/AggSite/PostList.aspx'      
        page = crawler.post_html(url,{"CategoryType":"Expert","ParentCategoryId":0,"CategoryId":-3,"PageIndex":i,"TotalPostCount":0,"ItemListActionName":"PostList"})       
        linkpattern = re.compile(u'<a class="titlelnk" href="http://www.cnblogs.com/(.*?)/archive/.*?" target="_blank">', re.S | re.U)
        links = linkpattern.findall(page)    
        for link in links:
            print link
            db.insert('insert ignore into bloglist(type,name) values(%s,%s)',('cnblog',link));   
        #mysql.insert('insert into bloglist(type,name) values(%s,%s)',('cnblog',_name));   
    