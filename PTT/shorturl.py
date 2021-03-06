#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= 'Jun 01, 2014 '
__author__= 'mkfsn'

import sys

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

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


def queryCheckshorturl(url):
    r = requests.post("http://checkshorturl.com/expand.php", data={"u":url})
    if r.status_code == 200:
        d = pq(r.text)
        p = d("table tr:nth-child(1) td:nth-child(2) a")
        return pq(p).attr("href")
    else:
        print "Error: " + r.status_code

def redirectURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
        'Pragma': 'no-cache',
        'Connection' : 'keep-alive'
        }
    try:
        r = requests.head(url, headers=headers)
    except requests.exceptions.ConnectionError as e:
        info = bcolors.FAIL + '[ %s ] %s\n'%(-1, url) + bcolors.ENDC
        sys.stderr.write(info)
        return {"url":'', "status":-1}

    if str(r.status_code)[0] == '3':
        info = bcolors.BLUE + '[ %s ] %s %s\n'%(r.status_code, url, r.headers['location']) + bcolors.ENDC
    elif str(r.status_code)[0] == '2':
        info = bcolors.GREEN + '[ %s ] %s\n'%(r.status_code, url) + bcolors.ENDC
    else:
        info = bcolors.HEADER + '[ %s ] %s\n'%(r.status_code, url) + bcolors.ENDC
    sys.stderr.write(info)

    res = {"url":'', "status":r.status_code}

    if 'location' in r.headers and r.headers['location']:
        res['url'] = r.headers['location']
    return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: ./shorturl.py [url]"
    else:
        # queryCheckshorturl(sys.argv[1])
        redirectURL(sys.argv[1])
