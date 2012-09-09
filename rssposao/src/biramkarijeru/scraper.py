#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib
import logging

from biramkarijeru.classes.CustomHTMLParser import CustomHTMLParser

################################################################################

def stripPage(page):
    
    beginIndex = page.find('<div class="item">')
    if beginIndex != -1:
        
        endIndex = page.find('<div class="paginator_bottom">', beginIndex)
        if endIndex != -1:
            return page[beginIndex : endIndex]

    return ''

################################################################################

currentPage = 1
while True:
    
    url = 'http://www.biramkarijeru.hr/index.php?cmd=search_oglas&&so_category=&so_region=0&so_word_mesh=&_page=' + str(currentPage)
    
    logging.info('Scraping URL: ' + url)
    
    page = urllib.urlopen(url).read()
    page = stripPage(page)
    
    if len(page) == 0:
        break
    
    try:
        
        htmlParser = CustomHTMLParser()
        htmlParser.feed(page)
        htmlParser.close()
        
    except:
        break
    
    currentPage += 1

logging.info('Done!')