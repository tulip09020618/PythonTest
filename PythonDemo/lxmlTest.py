#!usr/bin/python
# -*- coding : utf-8 -*-

from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
print(text)

print("------------------------------")
html = etree.HTML(text)
print(etree.tostring(html))

print("------------------------------")
result = html.xpath('//li')
print(result)
print(len(result))
print(type(result))
print(type(result[0]))

print("------------------------------")
result = html.xpath('//li/@class')
print(result)

print("------------------------------")
result = html.xpath('//li/a[@href="link1.html"]')
print(result)

print("------------------------------")
result = html.xpath('//li//span')
print(result)

print("------------------------------")
result = html.xpath('//li/a//@class')
print(result)

print("------------------------------")
result = html.xpath('//li[last()]/a/@href')
print(result)

print("------------------------------")
result = html.xpath('//li[last()-1]/a')
print(result[0].text)

print("------------------------------")
result = html.xpath('//*[@class="bold"]')
print(result[0].tag)

print("------------------------------")
result = html.xpath('//ul/li/attribute::class')
print(result)