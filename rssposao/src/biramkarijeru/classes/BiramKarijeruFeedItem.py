from google.appengine.ext import db

"""
"""
class BiramKarijeruFeedItem(db.Model):
    
    title       = db.StringProperty()
    link        = db.StringProperty()
    description = db.TextProperty()
    pubDate     = db.DateTimeProperty(auto_now_add=True)
    
    applicationDeadline = db.DateProperty()
