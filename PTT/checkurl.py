#!/usr/bin/python

import re 
import sys
import shorturl
import time
import sqlite3
import os

infile = open('Gossipurl.txt','r')
outfile = open('sh_Gossipurl.txt','w+')
outfile2 = open('lg_Gossipurl.txt','w+')
database = 'urls.db'

if os.path.isfile(database):
    con = sqlite3.connect(database)
    con.text_factory = str
    cursor = con.cursor()
else:
    print "Database not found"
    sys.exit(0)

for url in infile:
  url = url.split('\n')[0]

  page = re.match("^[0-9]",url)
  ppturl = re.match("^https?://ppt.cc/", url)
  goourl = re.match("^https?://goo.gl/", url)
  orzurl = re.match("^https?://0rz.tw/", url)
  youtuurl = re.match("^https?://youtu.be/", url)
  fburl = re.match("^https?://fb.com/", url)
  bitlyurl = re.match("^https?://bit.ly/", url)
  bitlyurl2 = re.match("^https?://bitly.com/", url)
  tinyurl = re.match("^https?://tinyurl.cm/", url)
  xcourl = re.match("^https?://x.co/", url)
  twitter = re.match("^https?://t.co/", url)

  if page : 
    outfile.write(url)
    print url
    continue

  flag = False
  if flag or ppturl or goourl or orzurl or youtuurl or fburl or bitlyurl or bitlyurl2 or tinyurl or xcourl or twitter:
    # Search database
    cursor.execute('SELECT * FROM urls WHERE entry = ?', (url,))
    result = cursor.fetchall()

    if len(result) == 0:
      shurl = shorturl.redirectURL(url)
      # ShortURL, OriginURL, StatusCode
      cursor.execute("INSERT INTO urls VALUES (?,?,?)", (url, shurl['url'], shurl['status'],))
      con.commit()
    elif  result[0][1] is '':
      pass
    else:
      #print "Already exists: ", url,
      pass
    # outfile.write('\n')
  else :
    # outfile2.write(url)
    # print "else: ", url
    #print "Not shorturl: ", url
    pass
  #time.sleep(1)  

infile.close()
outfile.close()
outfile2.close()
