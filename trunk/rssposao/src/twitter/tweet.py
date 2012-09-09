#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging

import base64
import urllib
import urllib2
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from twitter.classes.TweetData import TweetData

################################################################################

"""
"""
class Tweet(webapp.RequestHandler):
    
    """
    """
    def getTweetData(self, shortURL):
        return db.GqlQuery("SELECT * FROM TweetData "
                           "WHERE shortURL = :1 "
                           "AND isTweeted = :2", shortURL, False)
        
    """
    """
    def getMessage(self, tweetData):
        message  = tweetData.title + "; "
        message += tweetData.shortURL
        
        if len(tweetData.deadline) > 0:
            message += " Rok prijave: " + tweetData.deadline + ";"
            
        if len(tweetData.workplace):
            message += " Mjesto rada: " + tweetData.workplace
        
        if len(message) > 140:
            message = message[0:136] + "..."
            
        return message.encode("utf-8")
    
    """
    """
    def getAuthorizationString(self):
        
        username = ""
        password = ""
        
        return base64.encodestring('%s:%s' % (username, password))[:-1]
    
    
    """
    """
    def getParameters(self, message):

        parameters = {"status" : message }
        return urllib.urlencode(parameters)
    
    
    """
    """
    def tweet(self, tweetData):
        
        message    = self.getMessage(tweetData)

        parameters = self.getParameters(message)
        requestURL = "http://twitter.com/statuses/update.json"
        authString = self.getAuthorizationString()
        
        request = urllib2.Request(requestURL, parameters)
        request.add_header("Authorization", "Basic %s" % authString)
        
        response = urllib2.urlopen(request).read()
        
    
    """
    """
    def post(self):
        
        shortURL = self.request.get("shortURL")
        records  = self.getTweetData(shortURL)
        for tweetData in records:
            self.tweet(tweetData)
            
            tweetData.isTweeted = True
            tweetData.put()


"""
"""
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    wsgiref.handlers.CGIHandler().run(
        webapp.WSGIApplication([("/twitter/tweet", Tweet)]))


"""
"""
if __name__ == "__main__":
    main()