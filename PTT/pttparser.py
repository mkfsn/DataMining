#!/usr/bin/python
import pycurl
import HTMLParser
import re
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')
start = 550
stop = 4500

target_agent = "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.2.15 Version/10.00"

class GetPage:
  def __init__ (self,url):
    self.contents = ''
    self.url = url
  def read_page (self,buf):
    self.contents = self.contents + buf
  def show_page (self):
    print self.contents

class GetPageByFakeBrowser(GetPage):
  def __init__ (self, url, ua):
    self.contents = ''
    self.url = url
    self.ua = ua

class URLParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.urls = []
    self.links = []
  def handle_starttag(self, tag, attributes):
    if tag != 'a':return
    for name, value in attributes:
      if name == 'href' and value not in self.urls:
        article = re.match("^/bbs/Gossiping/M.",value)
        outlink = re.match("^((http|https):\/\/)",value)
        pttlink = re.match("^((http|https):\/\/)?www.ptt.cc",value)
        if article:
          self.urls.append(value)
        if outlink and not pttlink:
          self.links.append(value)


def crawler(url,mode):  # 0: links to artical, 1: links to outside ptt
  mypage = GetPageByFakeBrowser(url,target_agent)
  testcurl = pycurl.Curl()
  testcurl.setopt(testcurl.COOKIE,'over18=1')
  testcurl.setopt(testcurl.URL,mypage.url)
  testcurl.setopt(testcurl.USERAGENT, mypage.ua)
  testcurl.setopt(testcurl.WRITEFUNCTION,mypage.read_page)
  #testcurl.setopt(testcurl.VERBOSE,True)
  testcurl.perform()
  testcurl.close()
  parser = URLParser()
  parser.feed( mypage.contents)
  if mode:
    for links in parser.links:
      linklist.append(links)
  else:
    for url in parser.urls:
      origin = 'http://www.ptt.cc'+ url
      articals.append(origin)


outfile = open('Gossipurl.txt','w')
while start != stop:
  outfile.write(str(start))
  outfile.write('\n')
  articals = []
  linklist = []
  target_url = "http://www.ptt.cc/bbs/Gossiping/index" + str(start) + ".html" 
  crawler(target_url,0)
  start = start + 1
  time.sleep(1)

  for url in articals:
    print url
    crawler(url,1)

  for link in linklist:
    outfile.write(link)
    outfile.write('\n')

outfile.close()


