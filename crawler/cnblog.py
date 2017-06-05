#-*- encoding:UTF-8 -*-
from tools.CrawlerBase import *
                            
def extract(page):
    if page is None:
        return (None,None,None)

    linkpattern = re.compile(u'class="postTitle2" href="(.*?)">', re.S | re.U)
    links = linkpattern.findall(page)    
    return (links)

def process_article(article):
    title = ''
    body = ''
    post_date=''
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

    print 'title=',title
    return (title, body.strip(), post_date)

def insert_db(dt,link, title, body):
    sql=''
    title = title.replace("\r", u'')
    body = body.replace("\n", u'')
    print link
    print title
    print body

    
if __name__ == '__main__':   
    crawler = CrawlerBase()
    crawler.start('http://www.cnblogs.com/buptzym/default.html?page=%s',extract,process_article,insert_db)
