# -*- coding: utf-8 -*-
# python2.7.10

import urllib2
import HTMLParser
from bs4 import BeautifulSoup
import re
import sys

imdburl = "http://www.imdb.com"
baseurl = "http://www.imdb.com/title/"
taglst = []

def get_IMDbURL_from_douban(doubanurl):
    iurl = ''
    urlrequest = urllib2.Request(doubanurl)
    html_src = urllib2.urlopen(urlrequest).read()
    parser = BeautifulSoup(html_src, "html.parser")
    arr = parser.findAll('span', 'pl')
    for pl in arr:
        if pl.text.find('IMDb') > -1:
            iurl = pl.findNext('a')['href']
    return iurl

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
    # countries = parser.findAll('a', {'href' : re.compile(r'\?countries=')}) # Countries
    countries = parser.findAll('a', {'href' : re.compile(r'\?country_of_origin=')}) # Countries
    for country in countries:
        taglst.append(country.text.replace(' ', ''))
    try: # Release Date
        taglst.append(parser.find('div', 'subtext').findNext('meta', {'itemprop' : 'datePublished'})['content'].split('-')[0])
    except:
        taglst.append(parser.find('div', 'title_wrapper').findNext('span').findNext('a').text)
        # taglst.append(re.findall("\d+", parser.find('div', 'subtext').find('a', {'href' : re.compile(r'releaseinfo')}).text)[0]) # 20 April 2018
    genres = parser.findAll('a', {'href' : re.compile(r'/search/title\?genres')}) # Genres
    for genre in genres:
        if not genre.text.strip() in taglst:
            taglst.append(genre.text.strip())
    comoreurl = imdburl + parser.find('a', {'href' : re.compile(r'companycredits')})['href'] # Production Co
    # failed on "Show detailed company contact information on IMDbPro"
    # "http://www.imdb.com/title/tt1997605/companycredits?ref_=tt_ql_dt_5"
    urlrequest = urllib2.Request(comoreurl)
    html_src = urllib2.urlopen(urlrequest).read()
    parser = BeautifulSoup(html_src, "html.parser")
    prod = parser.find('h4', {'id' : 'production', 'name' : 'production'})
    if prod != None:
        prodinfo = prod.findNext('ul', 'simpleList')
        comps = prodinfo.findAll('a', {'href' : re.compile(r'/company/')})
        for comp in comps:
            taglst.append(comp.text.replace(' ', ''))
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
