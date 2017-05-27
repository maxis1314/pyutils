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

    def get_logger(self):
        return self.log

qinglog = logger('qingblog').get_logger()
#设置一下主页链接
oz_url = 'http://blog.sina.com.cn/blog'
conn = sqlite3.connect('qingblog.db')
cu=conn.cursor()


#init table 
cursor = conn.cursor()        
cursor.execute("create table if not exists oz(id integer primary key,link varchar(100),dt varchar(10),title varchar(100), body text NULL)")
conn.commit()
cursor.close()


sql=''
    
def gz_decode(data):
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data = gziper.read() 
    return data

def get_img(img_urls, img_path):
    for img_url in img_urls:
        s = re.search(u'/(\w+?\.jpg)', img_url, re.U)
        if s is None:
            continue
        img_name = s.group(1).strip()
        img_path.append(img_name)
        try:
            urllib.urlretrieve(img_url, img_name)
        except Exception,e:
            qinglog.error('get_img failed! url:%s, reason:%s' % (img_url, str(e)))
                          
def get_html(url):
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
        print qinglog.error('get_page failed, url:%s, reason:%s' % (url, str(e)))
        return None

def extract(page):
    if page is None:
        return (None,None,None)

    linkpattern = re.compile(u'class="postTitle2" href="(.*?)">', re.S | re.U)
    links = linkpattern.findall(page)    
    return (links,links,links)

def sub_div(m):
    content = ''
    if m is None:
        return ''
    content = m.group().strip()
    re.sub(u'<img.*?/>', '', content, flags = re.U | re.I | re.S)
    s = re.search(u'<div[\S ]*?>(.*?)<', content, re.U | re.S | re.I)
    if s is not None:
        return s.group(1).strip() + '\n'
    return ''

def process_article(article):
    title = ''
    body = ''
    img_urls = []
    
    titlepattern = re.compile(u'<a id="cb_post_title_url" class="postTitle2" href=".*?">(.*?)</a>', re.S | re.U)
    result = titlepattern.search(article)
    if result is not None:
        title = result.group(1).strip()
    
    bodypattern = re.compile(u'<div id="cnblogs_post_body">(.*?)</div><div id="MySignature">', re.S | re.U)
    result = bodypattern.search(article)
    if result is not None:
        body = result.group(1)

    imgpattern = re.compile(u'<span id="post-date">(.*?)</span>', re.S | re.U | re.I)
    result = imgpattern.search(article)
    if result is not None:
        post_date = result.group(1)

    return (title, body.strip(), post_date)

def insert_db(dt,link, title, body):
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
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        return True
    except Exception,e:
        qinglog.error('insert failed! sql:%s reason:%s' % (sql, str(e)))
        return False

def clear_oz():
    try:
        cursor = conn.cursor()
        cursor.execute('delete from oz')
        conn.commit()
        cursor.close()
        return True
    except Exception,e:
        qinglog.error('delete from oz failed! reason:%s' % (sql, str(e)))
        return False

if __name__ == '__main__':
    #print get_html('http://www.shanghaidaily.com/')
    #sys.exit()
    clear_oz()
    page = 1
    oz_url='http://www.cnblogs.com/bluescorpio/default.html?page='
    while True:
    #while page == 1:
        page_url = '%s%s' % (oz_url, str(page))
        qinglog.info('get page:%s' % page_url)
        page_html = get_html(page_url)
        
        if page_html is None:
            qinglog.info('%s is None' % page_url)
            page = page + 1
            continue       
        
        links,years,dates = extract(page_html)
        
        print links;
        if links is None or len(links) == 0:
            qinglog.info('no links or years or dates in %s' % page_url)
            break       
        
        if True:
            for link,year,date in zip(links,years,dates):
                #article_url = '%s/%s.html' % (oz_url, link)
                article_url = link
                article_page = get_html(article_url)
                if article_page is None:
                    qinglog.info('%s is None' % article_url)
                    page = page + 1
                    continue

                title, body, dt = process_article(article_page)                                
                title = title.replace('&amp;', '&')
                insert_db(dt,article_url, title.replace("'", "''"), body.replace("'", "''"))                            
        else:
            qinglog.info('length of years, dates, links not equal in %s' % page_url)
        page = page + 1

    conn.close()

                            
