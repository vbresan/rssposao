import logging
import string
import re

from datetime import datetime
from HTMLParser import HTMLParser

from BiramKarijeruFeedItem import BiramKarijeruFeedItem


"""
"""
class CustomHTMLParser(HTMLParser):
    
    """
    """
    def resetItemData(self):
        
        self.isItemOpened    = 0
        self.itemTitle       = ''
        self.itemLink        = ''
        self.itemDescription = ''
        
        self.lastClassAttribute = ''
        
    """
    """
    def setLastClassAttribute(self, attrs):
        
        if attrs.has_key('class'):
            self.lastClassAttribute = attrs['class']
    
    """
    """
    def isItemStart(self, tag, attrs):
        
        if len(self.currentPath) == 0:
            if tag.lower() == 'div':
                if attrs['class'].startswith('item'):
                    return True
        
        return False
    
    """
    """
    def isItemLink(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'a':
                if self.currentPath == '/div/div':
                    return True
            
        return False
       
    """
    """
    def isItemEnd(self):
        
        return len(self.currentPath) == 0 and self.isItemOpened
    
    """
    """
    def isItemTitle(self):
        
        if self.isItemOpened:
            if self.currentPath == '/div/div/a':
                if self.lastClassAttribute == 'naslov':
                    return True
            
        return False
    
    """
    """
    def isItemDescription(self):
        
        if self.isItemOpened:
            if self.currentPath.startswith('/div/div'):
                if self.lastClassAttribute == 'specs':
                    return True
                
        return False
    
    """
    """
    def isItemDescriptionEnd(self):
        
        if self.isItemOpened:
            if self.currentPath == '/div':
                if self.lastClassAttribute == 'specs':
                    return True
                
        return False
    
    """
    """
    def isItemNew(self):
        
        feedItems = BiramKarijeruFeedItem.gql("WHERE link = :1", self.itemLink)
        if feedItems.count() == 0: 
            return True
       
        return False
   
    """
    """
    def getExpireDate(self):
        
        descrption = self.itemDescription
        
        p = re.compile(r'Rok prijave:(.*)<br />', re.DOTALL)
        m = p.search(self.itemDescription)
        if m != None:
            return m.group(1).strip()
        
        return ''
    
    
    """
    """
    def saveItem(self):
        
        if self.isItemNew() == True:
            
            feedItem = BiramKarijeruFeedItem()
            
            feedItem.title       = self.itemTitle.strip().decode('utf-8')
            feedItem.link        = self.itemLink
            feedItem.description = self.itemDescription.decode('utf-8')
            
            applicationDeadline = self.getExpireDate()
            feedItem.applicationDeadline = datetime.strptime(applicationDeadline, '%d.%m.%Y').date()
            
            feedItem.put()
            logging.info('Saving item: ' + feedItem.title)
            
        else:
            
            raise Exception()
               
    """
    """
    def __init__(self):
        HTMLParser.__init__(self)

        self.currentPath = ''
        self.resetItemData()
        
        logging.info('Parsing page.')

    """
    """
    def handle_starttag(self, tag, attrs):
        
        attrs = dict(attrs)
        
        if self.isItemStart(tag, attrs):
            self.isItemOpened = 1
        elif self.isItemLink(tag, attrs):
            self.itemLink = 'http://www.biramkarijeru.hr' + attrs['href']
        
        self.setLastClassAttribute(attrs)
        self.currentPath += '/' + tag


    """
    """
    def handle_data(self, data):
        
        if self.isItemTitle():
            self.itemTitle += data + ' '
        elif self.isItemDescription():
            self.itemDescription += data + ' '
        

    """
    """
    def handle_endtag(self, tag):

        self.currentPath = string.rsplit(self.currentPath, '/', 1)[0]
        
        if self.isItemDescriptionEnd():
            self.itemDescription += '<br />\n'
        elif self.isItemEnd():
            self.saveItem()
            self.resetItemData()
