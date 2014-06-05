#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Jun 03, 2014 '
__author__= 'mkfsn'

import sys
import urllib2

try:
    import requests
except ImportError:
    print 'Please install requests.\nCommand:\n\t pip install requests'
    sys.exit(1)

try:
    from pyquery import PyQuery as pq
except ImportError:
    print 'Please install pyquery.\nCommand:\n\t pip install pyquery'
    sys.exit(1)


class parser:
    d = pq('<html></html>')
    def __init__ (self, url):
        attempt = 3
        while attempt:
            # Try three time
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', 'over18=1'))
            try:
                self.r = opener.open(url)
                self.d = pq(self.r.read())
                attempt = 0
            except urllib2.URLError, e:
                print e
                print url
                attempt = attempt - 1
                print "Try %d more ... " %(attempt)
            except urllib2.HTTPError, e:
                # Error occurs, try more
                attempt = attempt - 1
                print e
                print url
                print "Try %d more ... " %(attempt)
                self.d = pq("<html></html>")

        # self.cookies = dict(over18='1')
        # self.r = requests.get(url, cookies=self.cookies)
        # self.d = pq(self.r.text)
    # push
    def pushurl(self):
        self.p = self.d(".push a")
        urllist = []
        for i in self.p:
            link = pq(i).attr("href")
            parent = pq(i).parents(".push")
            userid = pq(parent).find(".push-userid").text()
            date   = pq(parent).find(".push-ipdatetime").text()
            urllist.append([userid, link, date])
        return urllist
    # main article
    def articleurl(self):
        self.p = self.d("#main-content > a")
        urllist = []
        for i in self.p:
            urllist.append( pq(i).attr("href") )
        return urllist
    # author
    def author(self):
        self.p = self.d(".article-metaline:eq(0) .article-meta-value")
        return self.p.text().split("(")[0].split(" ")[0]
    # title
    def title(self):
        self.p = self.d(".article-metaline:eq(1) .article-meta-value")
        return self.p.text()
    # datetime
    def datetime(self):
        self.p = self.d(".article-metaline:eq(2) .article-meta-value")
        return self.p.text()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
