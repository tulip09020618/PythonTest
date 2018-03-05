#!usr/bin/python
# -*- coding : utf-8 -*-

from pyquery import PyQuery as pq

doc = pq(filename='hello.html')
print(doc)

print("===================================")
print(doc.html())
print(type(doc))

print("===================================")
li = doc('li')
print(li)
print(type(li))
print(li.text())

print("===================================")
lis = doc('li')
for li in lis.items():
    print(li.html())

print("===================================")
print(lis.each(lambda e: e))