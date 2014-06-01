#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Jun 01, 2014 '
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
    r = requests.post("http://checkshorturl.com/expand.php", data={"u":url})
    if r.status_code == 200:
        d = pq(r.text)
        p = d("table tr:nth-child(1) td:nth-child(2) a")
        print pq(p).attr("href")
    else:
        print "Error: " + r.status_code

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: ./shorturl.py [url]"
    else:
        main(sys.argv[1])
