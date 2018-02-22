#!/usr/bin/python
# -*- coding: utf-8 -*-

import JRTime
import urllib2
import urllib

time = JRTime.JRTime()
print('当前时间：' + time.getCurrentTimeWithYmdHMS())

# 视频下载类
class VideoDownload:

    # 初始化
    def __init__(self):
        self.timeManager = JRTime.JRTime()

    def downloadVideo(self, videoUrl):
        print("视频下载地址：" + videoUrl)
        # 获取当前时间
        currentTime = self.timeManager.getCurrentTimeWithYmdHMS()
        # 保存到本地的视频名称
        videoName = currentTime + '.mp4'
        urllib.urlretrieve(videoUrl, videoName)




VideoDownload().downloadVideo("http://mov.bn.netease.com/mobilev/2011/9/8/V/S7CTIQ98V.mp4")