'''
Created on Jan 14, 2018

@author: mayijie
'''

import re

content = "<h2>abc</h2>pppppp<h3>def</h3>"
pattern = re.compile('<h2>(.*?)</h2>.*<h3>(.*?)</h3>', re.S)
items = re.findall(pattern,content)

print items[0][0], items[0][1]


'''

a = '''asdfsafhellopass:
    234455
    worldafdsf
    '''
b = re.findall('hello(.*?)world',a)
c = re.findall('hello(.*?)world',a,re.S)
print 'b is ' , b
print 'c is ' , c

'''