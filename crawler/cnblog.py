#-*- encoding:UTF-8 -*-
from tools.CrawlerBase import *
from tools.MysqlBase import *                          
import sys
import urlparse
import json 

db = MysqlBase('python')
count = 0;
crawlernew = CrawlerBase()

def extract(page):
    if page is None:
        return (None,None,None)

    linkpattern = re.compile(u'id=".*?List_TitleUrl_.*?".*?href="(.*?)">', re.S | re.U)
    links = linkpattern.findall(page)    
    return (links)

def process_article(article,link):
    title = ''
    body = ''
    dt=''
    img_urls = []
    
    titlepattern = re.compile(u'<a id="cb_post_title_url".*?href=".*?">(.*?)</a>', re.S | re.U)
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
        dt = result.group(1)
        
    
    imgpattern = re.compile(u'cb_blogId=([0-9]+),', re.S | re.U | re.I)
    result = imgpattern.search(article)
    if result is not None:
        bloggerid = result.group(1)
        
    print 'title=',title.encode('gb2312')
    
    title = title.replace('&amp;', '&')
    title = title.replace("'", "''")
    body = body.replace("'", "''").strip()                  

    postId = link.split('.')[2].split('/')[-1]
    
    url2 = u'http://www.cnblogs.com/mvc/blog/CategoriesTags.aspx?blogApp=gavin-cn&blogId='+bloggerid+'&postId='+postId+'&_='
    
    
    global db,count,crawlernew
    

    locations = json.loads(crawlernew.get_html(url2)) 
    tags = locations['Tags']
    categories = locations['Categories']
    
    
    linkpattern = re.compile(u'>(.*?)<', re.S | re.U)
    tags = linkpattern.findall(tags)
    categories = linkpattern.findall(categories)
    
    tags = set(tags)
    tags = list(tags)

    categories = set(categories)
    categories = list(categories)

    
    print 'categories=',categories
    print 'tags=',tags
    
    sql=''
    count=count+1
    if count%20==0:
        db.connect()
    title = title.replace("\r", u'')
    body = body.replace("\n", u'')
    db.insert('insert ignore into blog(dt,link,title,body,tags,categories,bid) values(%s,%s,%s,%s,%s,%s,%s)',(dt,link, title, body,','.join(tags),','.join(categories),bloggerid));

    
if __name__ == '__main__':
    name = sys.argv[1]
    if name is not None:
        crawler = CrawlerBase()
        crawler.start(u'http://www.cnblogs.com/'+name+'/default.html?page=%s',extract,process_article)
    else:
        print 'name is none'
