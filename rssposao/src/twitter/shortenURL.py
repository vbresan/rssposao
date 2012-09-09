#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging

import urllib
import wsgiref.handlers

from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from twitter.classes.TweetData import TweetData

################################################################################

"""
"""
class ShortenURL(webapp.RequestHandler):
    
    """
    """
    def getTweetData(self, longURL):
        return db.GqlQuery("SELECT * FROM TweetData "
                           "WHERE longURL = :1 "
                           "AND shortURL = :2", longURL, "")
    
    """
    """
    def getRequestURL(self, longURL):
        
        requestURL  = "http://api.bit.ly/shorten?"
        requestURL += "login="
        requestURL += "&apiKey="
        requestURL += "&version=2.0.1"
        requestURL += "&format=text"
        requestURL += "&longUrl=" + longURL
        
        return requestURL 
        
    """
    """
    def getShortURL(self, longURL):
        requestURL = self.getRequestURL(longURL)
        response   = urllib.urlopen(requestURL).read()
        
        return response
    
    """
    """
    def post(self):
        
        longURL = self.request.get("longURL")
        
        records = self.getTweetData(longURL) 
        if records.count(1000) > 0:
           shortURL = self.getShortURL(longURL)
           
           for tweetData in records:
               tweetData.shortURL = shortURL
               tweetData.put()
               
           taskqueue.Queue("twitter").add(taskqueue.Task(
                url    = "/twitter/tweet", 
                params = {"shortURL": shortURL}
            ))


"""
"""
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    wsgiref.handlers.CGIHandler().run(
        webapp.WSGIApplication([("/twitter/shortenURL", ShortenURL)]))


"""
"""
if __name__ == "__main__":
    main()