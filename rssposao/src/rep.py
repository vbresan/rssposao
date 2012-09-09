#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import sys
import PyRSS2Gen

from google.appengine.api import urlfetch

from classes.RepHTMLParser import RepHTMLParser

################################################################################

def stripPage(page):
    
    beginIndex = page.find('<div id="center">') + len('<div id="center">')
    if beginIndex != -1:
        
        endIndex = page.find('<div id="right">', beginIndex)
        if endIndex != -1:
            return page[beginIndex : endIndex]
        
    return ''

################################################################################

rss = PyRSS2Gen.RSS2(
        title = 'REP.hr - novi poslovi',
        link  = 'http://rep.hr',
        description = 'Novi poslovi na REP.hr',
        generator = 'http://www.rssposao.com',
        docs = ''
      )

page = urlfetch.fetch('', None, urlfetch.GET, {}, False, True, 10).content
page = stripPage(page)

htmlParser = RepHTMLParser(rss)
htmlParser.feed(page)
htmlParser.close()

print 'Content-Type: application/rss+xml'
rss.write_xml(sys.stdout, 'utf-8')