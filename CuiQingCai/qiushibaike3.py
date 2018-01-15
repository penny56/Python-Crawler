'''
Created on Jan 15, 2018

@author: mayijie
'''

import re, urllib2

class qsbk:
    
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # init headers
        self.headers = {'User-Agent' : self.user_agent}
        # each element is a page of duanzi
        self.stories = []
        # is the progress continue?
        self.enable = False
    
    # start to parse the pages
    def start(self):
        print u"Reading the Qiushibaike, press 'Enter' to continue, press 'Q' to quit"
        # set the enable to True
        self.enable = True
        # load the 1st page
        self.loadPage()
        # control the current page
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # get one page of stories from the list
                pageStories = self.stories[0]
                # plus the current page
                nowPage += 1
                # delete the used page
                del self.stories[0]
                # show the page
                self.getOneStory(pageStories, nowPage)
    
    # load the page and add to the list
    def loadPage(self):
        # if unread number of pages less than two, load new
        if self.enable:
            if len(self.stories) < 2:
                # get a new page
                pageStories = self.getPageItems(self.pageIndex)
                # put the new page to the list
                if pageStories:
                    self.stories.append(pageStories)
                    # add page index, for our next reading
                    self.pageIndex += 1 
    
    # for one dedicate page, parse the content and get the duanzi
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load fail..."
            return None
        pattern = re.compile('<div class="article block.*?<div class="author.*?<h2>(.*?)</h2>.*?'+
                             '<span>(.*?)</span>', 
                             re.S)
        items = re.findall(pattern, pageCode)
        # for store the duanzi
        pageStories = []
        # parse the items
        for item in items:
            # remove the <br/>
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            # item[0] is the publisher and item[1] is the duanzi content
            pageStories.append([item[0].strip(), text.strip()])
        return pageStories
            
    # get one dedicate page, return the row page
    def getPage(self, pageIndex):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # build the request
            request = urllib2.Request(url, headers = self.headers)
            # get the page code
            response = urllib2.urlopen(request)
            # transfer to utf-8 code
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u'Connect the url fail, reason:', e.reason
                return None
            
    # print a duanzi for every enter
    def getOneStory(self, pageStories, page):
        # retrieve on page of duanzi
        for story in pageStories:
            # wait for user input
            input = raw_input()
            # judge if need load new page
            self.loadPage()
            # input Q for quit
            if input == "Q":
                self.enable = False
                return
            print u"Page: %d\tAuthor: %s\t%s" %(page, story[0], story[1])

spider = qsbk()
spider.start()