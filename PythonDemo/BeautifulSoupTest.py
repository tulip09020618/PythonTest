#!usr/bin/python
# -*- coding: utf-8 -*-

import BeautifulSoup
import urllib2

request = urllib2.Request('https://cuiqingcai.com/1319.html')
try:
    response = urllib2.urlopen(request)
except urllib2.URLError, e:
    print(e)
# print(response.read().decode('utf-8'))

soup = BeautifulSoup.BeautifulSoup(unicode(response.read().decode('utf-8')))
# print(soup.text)
# print(soup.prettify())
print soup.div
print soup.div.contents