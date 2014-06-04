#!/usr/bin/python

import os, sys
import re 
import shorturl
import sqlite3

infile = open('Gossipurl.txt','r')
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

  r_list = [
    re.compile("^https?://ppt.cc/"),
    re.compile("^https?://goo.gl/"),
    re.compile("^https?://0rz.tw/"),
    re.compile("^https?://youtu.be/"),
    re.compile("^https?://fb.com/"),
    re.compile("^https?://bit.ly/"),
    re.compile("^https?://bitly.com/"),
    re.compile("^https?://tinyurl.cm/"),
    re.compile("^https?://x.co/"),
    re.compile("^https?://t.co/")
  ]

  if page : 
    print url
    continue

  flag = False
  if flag or any(r.match(url) for r in r_list):
    # Search database
    cursor.execute('SELECT * FROM urls WHERE entry = ?', (url,))
    result = cursor.fetchall()

    if len(result) == 0:
      shurl = shorturl.redirectURL(url)
      # ShortURL, OriginURL, StatusCode
      cursor.execute("INSERT INTO urls VALUES (?,?,?)", (url, shurl['url'], shurl['status'],))

    elif  result[0][1] is '':
      pass
    else:
      #print "Already exists: ", url,
      pass
  else:
    # print "\033[1;31m" + url + "\033[0m"
    cursor.execute("INSERT OR IGNORE INTO urls VALUES (?,?,?)", (url, url, 200,))

  con.commit()

con.close()
