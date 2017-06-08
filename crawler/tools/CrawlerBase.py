#-*- encoding:UTF-8 -*-
import urllib2
import re
import StringIO
import gzip
import logging
import sqlite3
import logutils
import urllib
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class logger:
    def __init__(self, name):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        fmt = '%(asctime)s %(filename)s:%(lineno)s %(name)s %(levelname)s :%(message)s'
        formatter = logging.Formatter(fmt)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        #fh = logging.FileHandler('qingblog.log')
        #fh.setFormatter(formatter)
        #fh.setLevel(logging.DEBUG)
        
        #self.log.addHandler(fh)
        self.log.addHandler(ch)
        self.sql=''

    def get_logger(self):
        return self.log

class CrawlerBase:
    def __init__(self):   
        self.qinglog = logger('qingblog').get_logger()       
        self.conn = sqlite3.connect('qingblog.db')
        #init table 
        cursor = self.conn.cursor()        
        cursor.execute("create table if not exists oz(id integer primary key,link varchar(100),dt varchar(10),title varchar(100), body text NULL)")
        self.conn.commit()
        cursor.close()
    
    def gz_decode(self,data):
        compressedstream = StringIO.StringIO(data)  
        gziper = gzip.GzipFile(fileobj=compressedstream)    
        data = gziper.read() 
        return data

                          
    def get_html(self,url):
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:35.0) Gecko/20100101 Firefox/35.0',\
                    'Accept': 'text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',\
                    #'Accept-Encoding': 'gzip, deflate',\
                    'Connection': 'keep-alive'}
            request = urllib2.Request(url, None, header)
            response = urllib2.urlopen(request)
            result = response.read()
            return result;
            #return gz_decode(result).decode('GBK')#.decode('UTF-8')
        except Exception,e:
            print self.qinglog.error('get_page failed, url:%s, reason:%s' % (url, str(e)))
            return None
    def post_html(self,url,values):
        data = urllib.urlencode(values)
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:35.0) Gecko/20100101 Firefox/35.0',\
                    'Accept': 'text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',\
                    #'Accept-Encoding': 'gzip, deflate',\
                    'Connection': 'keep-alive'}
            request = urllib2.Request(url, data, header)
            response = urllib2.urlopen(request)
            result = response.read()
            return result;
            #return gz_decode(result).decode('GBK')#.decode('UTF-8')
        except Exception,e:
            print self.qinglog.error('get_page failed, url:%s, reason:%s' % (url, str(e)))
            return None
    def extract(self,page):
        if page is None:
            return (None,None,None)

        linkpattern = re.compile(u'class="postTitle2" href="(.*?)">', re.S | re.U)
        links = linkpattern.findall(page)    
        return (links,links,links)

    def process_article(self,article):
        title = ''
        body = ''
        img_urls = []
        
        titlepattern = re.compile(u'<a id="cb_post_title_url" class=".*?" href=".*?">(.*?)</a>', re.S | re.U)
        result = titlepattern.search(article)
        if result is not None:
            title = result.group(1).strip()
        bodypattern = re.compile(u'<div id="cnblogs_post_body"[^>]*?>(.*?)</div><div id="MySignature">', re.S | re.U)
        result = bodypattern.search(article)
        if result is not None:
            body = result.group(1)

        imgpattern = re.compile(u'<span id="post-date">(.*?)</span>', re.S | re.U | re.I)
        result = imgpattern.search(article)
        if result is not None:
            post_date = result.group(1)

        return (title, body.strip(), post_date)

    def insert_db(self,dt,link, title, body):
        sql=''
        title = title.replace("\r", u'')
        body = body.replace("\n", u'')
        insert = u'insert into oz(dt'
        values = u"values(" + u"'" + dt + u"'"
        if link is not None and len(link) > 0:
            insert = insert + u', link'
            values = values + u", '" + link + u"'"
        if title is not None and len(title) > 0:
            insert = insert + u', title'
            values = values + u", '" + title + u"'"
        if body is not None and len(body) > 0:
            insert = insert + u', body'
            values = values + u", '" + body + u"'"    
        sql = insert + u')' + values + u')'
        #qinglog.info(sql)    
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
            return True
        except Exception,e:
            self.qinglog.error('insert failed! sql:%s reason:%s' % (sql, str(e)))
            return False

    def clear_oz(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('delete from oz')
            self.conn.commit()
            cursor.close()
            return True
        except Exception,e:
            self.qinglog.error('delete from oz failed! reason:%s' % str(e))
            return False

    def start(self,oz_url,extract,process_article):                
        #if process_article is None:
        #    process_article = self.process_article
        #print get_html('http://www.shanghaidaily.com/')
        #sys.exit()
        self.clear_oz()        
        page = 1        
        while True:
        #while page == 1:
            page_url = oz_url % str(page)
            self.qinglog.info('get page:%s' % page_url)
            page_html = self.get_html(page_url)
            
            if page_html is None:
                self.qinglog.info('%s is None' % page_url)
                page = page + 1
                continue       
            links = extract(page_html)        
            
            if links is None or len(links) == 0:
                self.qinglog.info('no links or years or dates in %s' % page_url)
                break       
            
            if True:
                for link in links:
                    #article_url = '%s/%s.html' % (oz_url, link)
                    article_url = link
                    print link
                    article_page = self.get_html(article_url)
                    if article_page is None:
                        self.qinglog.info('%s is None' % article_url)
                        page = page + 1
                        continue

                    process_article(article_page,link)                                
                                                
            else:
                self.qinglog.info('length of years, dates, links not equal in %s' % page_url)
            page = page + 1

        self.conn.close()

                            
