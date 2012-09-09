#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

from google.appengine.api.labs import taskqueue
from twitter.classes.FeedURL import FeedURL

################################################################################

feedURLs = FeedURL.all()
for feedURL in feedURLs:
    taskqueue.add(url="/twitter/fetchFeed", params={"url": feedURL.url})
