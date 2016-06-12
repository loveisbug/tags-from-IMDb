# -*- coding: utf-8 -*-
# python2.7.10

import urllib
import urllib2
import HTMLParser
from bs4 import BeautifulSoup
import sys

baseurl = "http://www.imdb.com/title/"

def get_IMDbID_from_douban(url):
    return ''

def gen_imdburl(param):
    ttid = ''
    tturl = ''
    if param.find('movie.douban') > -1:
        ttid = get_IMDbID_from_douban(param)
    elif param.find('tt') == 0: # and len(param) == 7
        ttid = param
    elif param.find('imdb.com/title/tt') > -1:
        tturl = param
    else:
        print "URL error."
        return ''
    if ttid:
        tturl = baseurl + ttid
    return tturl

def gen_tags(url):
    return 'test'

def tags_from_IMDb(param):
    tturl = gen_imdburl(param)
    if tturl:
        tags = gen_tags(tturl)
        print tags

def main(argv):
    if len(argv) > 1:
        tags_from_IMDb(argv[1])
        return 0
    else:
        print "Please input the URL or the IMDb id."
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
