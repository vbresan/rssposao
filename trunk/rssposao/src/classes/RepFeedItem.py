from google.appengine.ext import db

"""
"""
class RepFeedItem(db.Model):
    
    link    = db.StringProperty()
    pubDate = db.DateTimeProperty(auto_now_add=True)