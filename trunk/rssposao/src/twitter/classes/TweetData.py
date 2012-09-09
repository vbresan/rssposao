from google.appengine.ext import db

"""
"""
class TweetData(db.Model):

    title     = db.StringProperty()
    longURL   = db.StringProperty()
    shortURL  = db.StringProperty()
    deadline  = db.StringProperty()
    workplace = db.StringProperty()
    isTweeted = db.BooleanProperty()
