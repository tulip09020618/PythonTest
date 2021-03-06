#!/usr/bin/python
# -*- coding: utf-8 -*-

import JRTime
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
        print("开始下载 " + currentTime)

        # 保存到本地的视频名称
        videoName = self.getVideoName(videoUrl)
        print("视频名称：" + videoName)

        urllib.urlretrieve(videoUrl, videoName, self.cbk)

        print("视频下载完成")

    # 根据视频播放地址，获取视频名称
    def getVideoName(self, videoUrl):
        items = videoUrl.split('/')
        return items[len(items)-1]

    # 下载进度回调
    def cbk(self, a, b, c):
        '''''回调函数
        @a:已经下载的数据块
        @b:数据块的大小
        @c:远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print '正在下载：%.2f%%' % per




videoPlayUrl = "http://vapi.hahalanqiu.com/2018/02/02/20180202173522778ikaa3f_1.mov"
VideoDownload().downloadVideo(videoPlayUrl)