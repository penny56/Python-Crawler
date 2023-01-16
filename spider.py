'''
Created on Jan 8, 2019

The spider script used to parsing the data on web site according to the search text in self.search parameter.
The web site url composed by "url + urlPrefix + index + urlSuffix" and the index increase progressively each loop.

The last got html page will be stored in the same directory and named page.html, you could use this file as an example to generate the pattern.


Usage:
python spider.py abc        // abc is the text want to be searched 


@author: mayijie
'''

import sys, re, urllib2
reload(sys)
sys.setdefaultencoding("utf-8")

class spider:

    def __init__(self, search):
        # parameters need update
        
        self.url = "http://www.820lu.net/"
        self.urlPrefix = "vod-type-id-1-pg-"
        self.urlSuffix = ""
        self.pattern = '<div class="DiscussionListItem">.*?<h3 class="DiscussionListItem-title">(.*?)</h3>'
        '''
        self.url = "https://883fa.com/html/"
        self.urlPrefix = "25/"
        self.urlSuffix = ".html"
        self.pattern = '<div class="title"><h5 class="text-overflow">.*?">(.*?)</a></h5>'
        '''
        self.pageIndex = 1
        self.pageIndexMax = 100

        
        # don't update
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # init headers
        self.headers = {'User-Agent' : self.user_agent}
        # each story is the set of items/stories in a web page
        self.stories = []
        # the search text is got and the title (key) and index (value) pair are stored in gotcha dict
        self.gotcha = {}
        # the key text for searching 
        self.search = search

    # start to parse the pages
    def start(self):
        print u"Start to parsing the web site..."
        
        i = self.pageIndex
        while i <= self.pageIndexMax:
            pageStories = self.getPageItems(i)
            if len(pageStories) > 0:
                for pageStory in pageStories:
                    # check if the story is match the search text
                    if re.search(self.search.decode("utf-8"), pageStory) != None:
                        self.gotcha[pageStory] = i
            i += 1
        
        print u"Here is the list:"
        for key, value in self.gotcha.items():
            print key + "==>" + value

    # for one dedicate page, parse the content and get the items/stories and return
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load fail..."
            return None

        # get the target text from page code according to the pattern, then strip the text and storied in the pageStories array
        patternStr = re.compile(self.pattern, re.S)
        items = re.findall(patternStr, pageCode)
        pageStories = []
        # parse the items
        for item in items:
            pageStories.append(item.strip())
        return pageStories

    # get one dedicate page, return the row page
    def getPage(self, pageIndex):
        try:
            url = self.url + self.urlPrefix + str(pageIndex) + self.urlSuffix
            print url
            # build the request
            request = urllib2.Request(url, headers = self.headers)
            # get the page code
            response = urllib2.urlopen(request)
            # transfer to utf-8 code
            pageCode = response.read().decode('utf-8')
            # YJ add for test
            with open ('page.html', 'w') as f:
                f.write(pageCode)
            # YJ
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u'Connect the url fail, reason:', e.reason
                return None

# main

if len(sys.argv) == 2:
    search = sys.argv[1]
else:
    print u"Parameter input error, you should specify a search text."

spider = spider(search)
spider.start()
