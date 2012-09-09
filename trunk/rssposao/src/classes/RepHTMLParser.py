import string
import re
import PyRSS2Gen

from RepFeedItem import RepFeedItem
from HTMLParser import HTMLParser

"""
"""
class RepHTMLParser(HTMLParser):
    
    """
    """
    def resetItemData(self):
        
        self.isItemOpened    = 0
        self.itemTitle       = ''
        self.itemLink        = ''
        self.itemDescription = ''
        
        self.currentClassAttribute = ''
        
    """
    """
    def setCurrentClassAttribute(self, attrs):
        
        if attrs.has_key('class'):
            self.currentClassAttribute = attrs['class']
        else:
            self.currentClassAttribute = ''
        
    
    """
    """
    def isItemStart(self, tag, attrs):
        
        if len(self.currentPath) == 0:
            if tag.lower() == 'div':
                if attrs['class'] == 'oglas' or attrs['class'].startswith('oglas oglas-mali'):
                    return 1
            elif tag.lower() == 'p':
                if attrs['class'] == 'ostali-oglasi':
                    return 1
        
        return 0
    
    """
    """
    def isItemLink(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'a':
                if self.currentPath == '/div/p' or self.currentPath == '/p':
                    return 1
            
        return 0
    
    """
    """
    def isLogo(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'img':
                if self.currentPath == '/div/p':
                    return 1
                
        return 0
    
    """
    """
    def isIcon(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'img':
                if self.currentPath == '/div/div/p':
                    return 1
                
        return 0
    
       
    """
    """
    def isItemEnd(self):
        
        return len(self.currentPath) == 0 and self.isItemOpened
    
    """
    """
    def isItemTitle(self):
        
        if self.isItemOpened:
            if self.currentPath == '/div/p/a' or self.currentPath == '/p/a':
                return 1
            
        return 0
    
    """
    """
    def isJobType(self):
        
        if self.isItemOpened:
            if self.currentPath == '/div/p':
                if self.currentClassAttribute == 'oglas-tip':
                    return 1
                
        return 0
    
    """
    """
    def isJobLocation(self):
        
        if self.isItemOpened:
            if self.currentPath == '/div/div/p':
                if self.currentClassAttribute == 'oglas-mjesto':
                    return 1
                
        return 0
    
    """
    """
    def saveFeedItem(self, itemLink):
        
        feedItem = RepFeedItem()
        feedItem.link = itemLink
        
        feedItem.put()
        
    
    """
    """
    def getItemPubDate(self, itemLink):
        
        feedItems = RepFeedItem.gql("WHERE link = :1", itemLink)
        if feedItems.count():
            return feedItems[0].pubDate
            
        self.saveFeedItem(itemLink)
        return self.getItemPubDate(itemLink)
    
    
    """
    """
    def appendItem(self):
        
        self.rss.items.append(PyRSS2Gen.RSSItem(
                                                
            title       = self.itemTitle.strip(), 
            link        = self.itemLink,
#            description = '<![CDATA[' + self.itemDescription + ']]>',
            description = self.itemDescription,
            pubDate     = self.getItemPubDate(self.itemLink)
        ))
        
    """
    """
    def getIconDescription(self, inputString):
        
        p = re.compile(r'Tip\(\'(.*)\',TITLE,\'(.*)\'\);')
        m = p.match(inputString)
        
        return m.group(2) + ': ' + m.group(1)
        
    
    """
    """
    def __init__(self, rss):
        HTMLParser.__init__(self)

        self.rss = rss    
            
        self.currentPath = ''
        self.resetItemData()

    """
    """
    def handle_starttag(self, tag, attrs):
        
        attrs = dict(attrs)
        
        if self.isItemStart(tag, attrs):
            self.isItemOpened = 1
        elif self.isItemLink(tag, attrs):
            self.itemLink = 'http://rep.hr' + attrs['href']
        elif self.isLogo(tag, attrs):
            self.itemDescription += '<img src="http://rep.hr' + attrs['src'] + '" /><br />\n'
        elif self.isIcon(tag, attrs):
            self.itemDescription += self.getIconDescription(attrs['onmouseover']) + '<br />\n'
        
        self.setCurrentClassAttribute(attrs)
        self.currentPath += '/' + tag


    """
    """
    def handle_data(self, data):
        
        if self.isItemTitle():
            self.itemTitle += data + ' '
        elif self.isJobType():
            self.itemDescription += 'Tip posla: ' + data + '<br />\n'
        elif self.isJobLocation():
            self.itemDescription += 'Mjesto rada: ' + data + '<br />\n'
        

    """
    """
    def handle_endtag(self, tag):

        self.currentPath = string.rsplit(self.currentPath, '/', 1)[0]
        
        if self.isItemEnd():
            
            self.appendItem()
            self.resetItemData()
