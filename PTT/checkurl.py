#!/usr/bin/python

import re 
import sys
import shorturl
import time

infile = open('Gossipurl.txt','r')
outfile = open('sh_Gossipurl.txt','w+')
outfile2 = open('lg_Gossipurl.txt','w+')
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
    print url
  if ppturl or goourl or orzurl or youtuurl or fburl or bitlyurl or bitlyurl2 or tinyurl or xcourl:
    shurl = shorturl.redirectURL(url)
    if shurl is not None : outfile.write(shurl)
    outfile.write('\n')
  else :
    outfile2.write(url)
  #time.sleep(1)  

infile.close()
outfile.close()
outfile2.close()
