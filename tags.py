# -*- coding: utf-8 -*-
# python2.7.10

import urllib
import urllib2
import HTMLParser
from bs4 import BeautifulSoup
import re
import sys

baseurl = "http://www.imdb.com/title/"
taglst = []

def get_IMDbURL_from_douban(doubanurl):
    imdburl = ''
    urlrequest = urllib2.Request(doubanurl)
    html_src = urllib2.urlopen(urlrequest).read()
    parser = BeautifulSoup(html_src, "html.parser")
    arr = parser.findAll('span', 'pl')
    for pl in arr:
        if pl.text.find('IMDb') > -1:
            imdburl = pl.findNext('a')['href']
    return imdburl

def gen_imdburl(param):
    ttid = ''
    tturl = ''
    if param.find('movie.douban') > -1:
        tturl = get_IMDbURL_from_douban(param)
    elif param.find('tt') == 0: # and len(param) == 7
        ttid = param
    elif param.find('imdb.com/title/tt') > -1:
        tturl = param
    else:
        print "URL error."
    if ttid:
        tturl = baseurl + ttid
    return tturl

def gen_tags(url):
    urlrequest = urllib2.Request(url)
    html_src = urllib2.urlopen(urlrequest).read()
    parser = BeautifulSoup(html_src, "html.parser")
    # country = parser.findAll('a', {'href' : re.compile(r'/country/')})
    # for cou in country:
    #     taglst.append(cou.text)
    taglst.append(parser.find('a', {'href' : re.compile(r'/country/')}).text) # Country
    taglst.append(parser.find('div', 'subtext').findNext('meta', {'itemprop' : 'datePublished'})['content'].split('-')[0]) # Release Date
    genres = parser.findAll('span', {'class' : 'itemprop', 'itemprop' : 'genre'})
    for genre in genres:
        taglst.append(genre.text)
    taglst.append(parser.find('a', {'href' : re.compile(r'/company/')}).text.replace(' ', '')) # Production Co
    return taglst

def tags_from_IMDb(param):
    tturl = gen_imdburl(param)
    if tturl:
        tags = gen_tags(tturl)
        print ' '.join(tags)

def main(argv):
    if len(argv) > 1:
        tags_from_IMDb(argv[1])
        return 0
    else:
        print "Please input the URL or the IMDb id."
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
