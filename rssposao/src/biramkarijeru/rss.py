#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import PyRSS2Gen
import sys

from datetime import date

from biramkarijeru.classes.BiramKarijeruFeedItem import BiramKarijeruFeedItem

################################################################################

rss = PyRSS2Gen.RSS2(
        title = 'BiramKarijeru.hr - novi poslovi',
        link  = 'http://www.biramkarijeru.hr',
        description = 'Novi poslovi na BiramKarijeru.hr',
        generator = 'http://www.rssposao.com',
        docs = ''
      )


today = date.today()
items = BiramKarijeruFeedItem.gql("ORDER BY pubDate DESC LIMIT 100")
for item in items:
    if item.applicationDeadline >= today:
        rss.items.append(PyRSS2Gen.RSSItem(
                                                    
                title       = item.title, 
                link        = item.link,
    #            description = '<![CDATA[' + item.description + ']]>',
                description = item.description,
                pubDate     = item.pubDate
            ))

print 'Content-Type: application/rss+xml'
rss.write_xml(sys.stdout, 'utf-8')
