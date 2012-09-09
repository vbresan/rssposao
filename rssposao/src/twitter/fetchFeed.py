#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import re
import urllib
import wsgiref.handlers
import xml.dom.minidom

from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from twitter.classes.TweetData import TweetData

################################################################################

"""
"""
class FetchFeed(webapp.RequestHandler):
    
    """
    """
    def getTitle(self, item):
        return item.getElementsByTagName("title")[0].firstChild.data
    
    """
    """
    def getLink(self, item):
        return item.getElementsByTagName("link")[0].firstChild.data
    
    """
    """
    def getDescription(self, item):
       return item.getElementsByTagName("description")[0].firstChild.data
    
    """
    """
    def getDeadline(self, description):
        
        deadline = ""
        
        m = re.search("Rok prijave: (.*)", description)
        if m is not None:
            deadline = m.group(1)
        else:
            m = re.search("Rok za prijavu: ([^<,]*)", description)
            if m is not None:
                deadline = m.group(1)
                
        if deadline.endswith("."):
            deadline = deadline[0:len(deadline) - 1]
            
        return deadline
    
    """
    """
    def getWorkplace(self, description):
        
        workplace = ""
        
        m = re.search("Mjesto rada: ([^<]*)", description)
        if m is not None:
            workplace = m.group(1);
            
        return workplace
    
    """
    """
    def saveTweetData(self, item):
        
        link  = self.getLink(item)
        found = db.GqlQuery("SELECT * FROM TweetData WHERE longURL = :1", link)
        if found.count(1) == 0:
            
            description = self.getDescription(item)
            
            tweetData = TweetData(
                title     = self.getTitle(item), 
                longURL   = link, 
                shortURL  = "", 
                deadline  = self.getDeadline(description), 
                workplace = self.getWorkplace(description), 
                isTweeted = False
            )
            
            tweetData.put()
            return tweetData
            
        return None
    
    """
    """
    def post(self):
        
        url = self.request.get("url")
        
        content = urllib.urlopen(url)
        doc = xml.dom.minidom.parse(content)

        items = doc.getElementsByTagName("item")
        for item in items:
            tweetData = self.saveTweetData(item)
            if tweetData != None:
                taskqueue.Queue("bitly").add(taskqueue.Task(
                    url    = "/twitter/shortenURL", 
                    params = {"longURL": tweetData.longURL}
                ))


"""
"""
def main():
    wsgiref.handlers.CGIHandler().run(
        webapp.WSGIApplication([("/twitter/fetchFeed", FetchFeed)]))


"""
"""
if __name__ == "__main__":
    main()