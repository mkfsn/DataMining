#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Jun 03, 2014 '
__author__= 'mkfsn'

import sys
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


def main(url):
    cookies = dict(over18='1')
    r = requests.get(url, cookies=cookies)
    d = pq(r.text)
    # push
    p = d(".push a")
    for i in p:
        link = pq(i).attr("href")
        userid = pq(i).parents(".push").find(".push-userid").text()
        print userid, ":", link
    # main article 
    p = d("#main-content > a")
    for i in p:
        print pq(i).attr("href")
    # author
    p = d(".article-metaline:eq(0) .article-meta-value")
    print p.text().split("(")[0]
    # title
    p = d(".article-metaline:eq(1) .article-meta-value")
    print p.text()
    # datetime
    p = d(".article-metaline:eq(2) .article-meta-value")
    print p.text()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
