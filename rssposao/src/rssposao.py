#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging
import string
import re
import urllib
import xml.dom.minidom

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

################################################################################

feedURLs        = { 'mojposao' : 'http://www.mojposao.net/rss.php' }

categoryStrings = { 'mojposao' : 
                        { '0'  : u'Nekategorizirano',
                          'm'  : u'Management',
                          '1'  : u'Računarstvo i Internet',
                          '2'  : u'Strojarstvo i elektrotehnika',
                          '3'  : u'Trgovina, prodaja i marketing',
                          '4'  : u'Ekonomija (opće)',
                          '5'  : u'Administrativna zanimanja',
                          '6'  : u'Pravo',
                          '7'  : u'Dizajn i umjetnost',
                          '8'  : u'Obrazovanje i briga o djeci',
                          '9'  : u'Promet i transport',
                          '10' : u'Građevina i arhitektura',
                          '11' : u'Zdravstvo i briga o ljepoti',
                          '12' : u'Turizam, ugostiteljstvo, prehr.',
                          '13' : u'Osobne usluge',
                          '14' : u'Ostalo',
                          'p'  : u'Državna služba i neprofitne organizacije',
                        } 
                  }

################################################################################

class Link(db.Model):
    url        = db.StringProperty()
    categoryID = db.StringProperty()
    accessTime = db.DateTimeProperty(auto_now=True)

################################################################################

def getFeedURL(siteID):
    return feedURLs[siteID]

################################################################################

def getCategoryString(siteID, categoryID):
    return categoryStrings[siteID][categoryID]

################################################################################

def getCategories(url, feedID):
    
    categories = []
    
    page = urllib.urlopen(url).read().decode('windows-1250')
    for categoryID in categoryStrings[feedID]:
        
        categoryString = getCategoryString(feedID, categoryID)
        if page.find('<dd>' + categoryString + '<br /></dd>') != -1:
            categories.append(categoryID)
            
    if len(categories) == 0 :
        categories.append(0)
    
    return categories
    
################################################################################

def saveLink(url, feedID):
    
    categories = getCategories(url, feedID)
    for categoryID in categories:
    
        link = Link()
        
        link.url        = url
        link.categoryID = str(categoryID)
        link.put()

################################################################################

def isLinkInCategory(url, feedID, categoryID):
    
    links = Link.gql("WHERE url = :1", url)
    if links.count() :
        
        for link in links:
            link.put()
            if link.categoryID == categoryID:
                return 1
        
        return 0;
    
    saveLink(url, feedID)
    return isLinkInCategory(url, feedID, categoryID)

################################################################################

def setNewTitle(parent, feedID, categoryID):
    
    categoryString = getCategoryString(feedID, categoryID)
    
    title = parent.getElementsByTagName('title')[0].firstChild.data
    title = string.replace(title, 'novi poslovi', categoryString)
    
    parent.getElementsByTagName('title')[0].firstChild.data = title

################################################################################

def getFilteredFeed(feedID, categoryID):
    
    feedURL = getFeedURL(feedID)
    doc = xml.dom.minidom.parse(urllib.urlopen(feedURL))

    parent = doc.getElementsByTagName('channel')[0]
    setNewTitle(parent, feedID, categoryID)

    items  = doc.getElementsByTagName('item')
    for item in items :
        link = item.getElementsByTagName('link')[0].firstChild.data
        
        if not isLinkInCategory(link, feedID, categoryID) :
            parent.removeChild(item)
    
    filtered = doc.toxml()
    
    pattern = re.compile(r'<description>(.*?)</description>', re.DOTALL)
    filtered = re.sub(pattern, r'<description><![CDATA[\1]]></description>', filtered)
    
    return filtered
    
################################################################################

def generateFeed(path):
    
    pathElements = path.split('/')
    
    feedID     = pathElements[1]
    categoryID = pathElements[2]
    
    return getFilteredFeed(feedID, categoryID)

################################################################################

class FeedGenerator(webapp.RequestHandler):
    def get(self):
        self.response.out.write(generateFeed(self.request.path))
    
    def post(self):
        self.response.out.write(generateFeed(self.request.path))

################################################################################
        
application = webapp.WSGIApplication([('/.*', FeedGenerator)], debug=True)

def main():
    
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)


if __name__ == "__main__":
  main()
