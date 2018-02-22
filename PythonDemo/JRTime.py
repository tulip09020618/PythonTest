#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

# 自定义时间处理类
class JRTime:

    # 获取当前时间2018-02-21 12:16:53
    def getCurrentTimeWithYmdHMS(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 获取当前日期
    def getCurrentDataWithYmd(self):
        return time.strftime('[%Y-%m-%d]', time.localtime(time.time()))
