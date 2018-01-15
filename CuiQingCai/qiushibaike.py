'''
Created on Jan 12, 2018

@author: mayijie
'''

#import urllib
import urllib2, re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)

# what's the header here for ???
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent}
try:
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    #print response.read()
    
    content = response.read().decode('utf-8')
    pattern = re.compile('<div class="article block.*?<div class="author.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>', re.S)
    items = re.findall(pattern,content)
    for item in items:
        print item[0] + "===>" + item[1]
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
except Exception, e:
    print e


