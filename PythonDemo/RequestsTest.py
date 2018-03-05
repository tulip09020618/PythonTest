#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

r = requests.get('http://cuiqingcai.com')
print(type(r))
print r.status_code
print r.encoding
print r.cookies

r = requests.get('https://kyfw.12306.cn/otn/', verify=False)
print r.text