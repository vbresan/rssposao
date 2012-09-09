from google.appengine.ext import db

"""
"""
class FeedURL(db.Model):

    title = db.StringProperty()
    url   = db.StringProperty();
