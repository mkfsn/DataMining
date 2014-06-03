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

  page = re.match("^[0-9]",url)
  ppturl = re.match("^http://ppt.cc", url) 
  goourl = re.match("^http://goo.gl", url) 
  orzurl = re.match("^http://0rz.tw", url) 
  youtuurl = re.match("^http://youtu.be", url) 
  fburl = re.match("^http://fb.com", url) 
  bitlyurl = re.match("^http://bit.ly", url) 
  bitlyurl2 = re.match("^http://bitly.com", url) 
  tinyurl = re.match("^http://tinyurl.com", url) 
  xcourl = re.match("^http://x.co", url)

  if page : 
    outfile.write(url)

  if ppturl or goourl or orzurl or youtuurl or fburl or bitlyurl or bitlyurl2 or tinyurl or xcourl:
    # Search database
    cursor.execute('SELECT * FROM urls WHERE entry = ?', (url,))
    result = cursor.fetchall()

    if len(result) == 0:
      shurl = shorturl.redirectURL(url)
      if shurl is not None:
        # outfile.write(shurl)
        cursor.execute("INSERT INTO urls VALUES (?,?)", (url, shurl,))
      else:
        cursor.execute("INSERT INTO urls VALUES (?,?)", (url, '',))
      con.commit()
    elif  result[0][1] is '':
      pass
    else:
      print "Already exists: ", url,
    # outfile.write('\n')
  else :
    # outfile2.write(url)
    # print "else: ", url
    print "Not shorturl: ", url
  #time.sleep(1)  

infile.close()
outfile.close()
outfile2.close()
