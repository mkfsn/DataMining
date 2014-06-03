#!/usr/bin/python
import pycurl
import HTMLParser
import re
import os,sys
import time
import query as q
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')
start = 550
stop = 4500

database = 'datamining'

if os.path.isfile(database):
  con = sqlite3.connect(database)
  con.text_factory = str
  cursor = con.cursor()

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
  def handle_starttag(self, tag, attributes):
    if tag != 'a' : return
    for name, value in attributes:
      if name == 'href' and value not in self.urls:
        article = re.match("^/bbs/Gossiping/M.",value)
        if article:
          self.urls.append(value)


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
  for url in parser.urls:
    origin = 'http://www.ptt.cc'+ url
    articals.append(origin)


while start != stop:
  print start
  articals = []
  linklist = []
  target_url = "http://www.ptt.cc/bbs/Gossiping/index" + str(start) + ".html" 
  crawler(target_url,0)
  start = start + 1
  #time.sleep(1)

  for alink in articals:
    cursor.execute("SELECT count(*) FROM ptt where alink = ?" , (alink,))
    r = cursor.fetchall()
    if r[0][0] != 0:
      continue 
    a = q.parser(alink)
    if a.articleurl():
      title = a.title()
      date = a.datetime()
      author = a.author()
      url = a.articleurl()
      cursor.execute("INSERT INTO ptt VALUES (?,?,?,?,?)", (title, date, author, url, alink,))
      con.commit()
    if a.pushurl():
      title = a.title()
      date = a.datetime()
      author = a.pushurl()[0]
      url = a.pushurl()[1]
      cursor.execute("INSERT INTO ptt VALUES (?,?,?,?,?)", (title, date, author, url, alink,))
      con.commit()

