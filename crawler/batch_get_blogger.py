#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *
from tools.CrawlerBase import *
import subprocess
import time 
if __name__ == '__main__':    
    crawler = CrawlerBase()
    db = MysqlBase('python')
    for i in range(200):
        url = u'https://www.cnblogs.com/sitehome/p/'+str(i+1)
        page = crawler.get_html(url)
        linkpattern = re.compile(u'<a class="titlelnk" href="http://www.cnblogs.com/(.*?)/p/.*?" target="_blank">', re.S | re.U)
        links = linkpattern.findall(page)    
        for link in links:
            print link
            db.insert('insert ignore into bloglist(type,name) values(%s,%s)',('cnblog',link));   
        #mysql.insert('insert into bloglist(type,name) values(%s,%s)',('cnblog',_name));   
    
