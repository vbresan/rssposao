#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

from twitter.classes.FeedURL import FeedURL

################################################################################

feedURLs = []
feedURLs.append(FeedURL(title='Moj Posao', url='http://feeds2.feedburner.com/MojPosao'))
feedURLs.append(FeedURL(title='Posao', url='http://www.posao.hr/rss/'))
feedURLs.append(FeedURL(title='HZZ', url='http://hzzweb.hzz.hr/rss/rss.xml'))
feedURLs.append(FeedURL(title='Biram Karijeru', url='http://www.biramkarijeru.hr/index.php?cmd=show_rss'))
feedURLs.append(FeedURL(title='REP', url='http://feeds2.feedburner.com/rep/novi-poslovi'))
feedURLs.append(FeedURL(title='ITjobr', url='http://www.itjobr.net/feed/rss/'))

for feedURL in feedURLs:
    feedURL.put()
