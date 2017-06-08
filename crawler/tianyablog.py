#-*- encoding:UTF-8 -*-
from tools.CrawlerBase import *
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

                            
def extract(page):
    if page is None:
        return (None,None,None)

    linkpattern = re.compile(u'<div class=\'article\'><h2><a href=\'(.*?)\' class=\'tj\' target=\'_blank\'>', re.S | re.U)
    links = linkpattern.findall(page)    
    return (links)

def process_article(article,link):   
    title = ''
    body = ''
    post_date=''
    img_urls = []
    
    titlepattern = re.compile(u'<h2><a href=".*?" class="tj" title="(.*?)">', re.S | re.U)
    result = titlepattern.search(article)
    if result is not None:
        title = result.group(1).strip()
    bodypattern = re.compile(u'<div class="article-summary articletext" >(.*?)</div><div class="article-categories pos-relative">', re.S | re.U)
    result = bodypattern.search(article)
    if result is not None:
        body = result.group(1)

    imgpattern = re.compile(u'<span class="pos-right gray6">(.*?)</span>', re.S | re.U | re.I)
    result = imgpattern.search(article)
    if result is not None:
        post_date = result.group(1)
    
    print 'title=',title.encode('gbk')    
    print (title, body.strip(), post_date)
    
    
if __name__ == '__main__':   
    crawler = CrawlerBase()
    crawler.start('http://blog.tianya.cn/blog-4698784-%s.shtml',extract,process_article)
