import requests
import bs4
import urllib.request
import urllib
import os
 
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
 
DownPath = "C:/Users/Administrator/PycharmProjects/untitled/"
 
c = '.jpg'
 
for x in range(5, 100):
 
    newDownPath = DownPath + str(x) +"/"
    os.mkdir(newDownPath)
    site = "http://www.meizitu.com/a/" + str(x) + ".html"
    local_filename, headers = urllib.request.urlretrieve(site)
    html = open(local_filename)
 
    soup = bs4.BeautifulSoup(html,"html5lib")
    jpg = soup.find_all('img')
 
    PhotoNum = 0
    for photo in jpg:
        src = photo.get('src')
        print(src)
 
        PhotoNum += 1
        Name = (str(PhotoNum) + c)
        r = requests.get(src,headers = hdr)
        with open(newDownPath + Name, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
        print(src)