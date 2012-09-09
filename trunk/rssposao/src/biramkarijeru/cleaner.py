#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging

from google.appengine.ext import db
from datetime import date

from biramkarijeru.classes.BiramKarijeruFeedItem import BiramKarijeruFeedItem

################################################################################

items = BiramKarijeruFeedItem.gql("WHERE applicationDeadline < :1", date.today())
for item in items:
    
    logging.info('Deleting expired item: ' + item.title + '(exp date: ' + item.applicationDeadline.isoformat() + ')')
    item.delete()
