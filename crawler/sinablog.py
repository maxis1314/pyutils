#-*- encoding:UTF-8 -*-
from tools.CrawlerBase import *
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

                            
def extract(page):
    if page is None:
        return (None,None,None)

    linkpattern = re.compile(u'<a title="" target="_blank" href="(.*?)">', re.S | re.U)
    links = linkpattern.findall(page)    
    return (links)

def process_article(article,link):   
    title = ''
    body = ''
    post_date=''
    img_urls = []
    
    titlepattern = re.compile(u'<h2 id=".*?" class="titName SG_txta">(.*?)</h2>', re.S | re.U)
    result = titlepattern.search(article)
    if result is not None:
        title = result.group(1).strip()
    bodypattern = re.compile(u'<div id="sina_keyword_ad_area2" class="articalContent   newfont_family">(.*?)<div id=\'share\' class="shareUp">', re.S | re.U)
    result = bodypattern.search(article)
    if result is not None:
        body = result.group(1)

    imgpattern = re.compile(u'<span class="time SG_txtc">\((.*?)\)</span>', re.S | re.U | re.I)
    result = imgpattern.search(article)
    if result is not None:
        post_date = result.group(1)
    
    print 'title=',title.encode('gbk')    
    print (title, body.strip(), post_date)
    return 'ok'
    
    
if __name__ == '__main__':   
    crawler = CrawlerBase()
    crawler.start('http://blog.sina.com.cn/s/articlelist_1259295385_0_%s.html',extract,process_article)
