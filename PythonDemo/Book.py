#!usr/bin/python
# coding:utf-8

from pyquery import PyQuery as pq
import Tool
import os


class Book:

    # 初始化方法
    def __init__(self, url, dir_path, file_name):
        self.tool = Tool.Tool()
        self.url = url
        self.host = "http://m.aoyuge.com"
        self.dir_path = dir_path
        self.file_name = file_name
        # 创建路径
        self.mkDir(self.dir_path)

    # 获取所有目录列表
    def getAllList(self, url):
        doc = pq(url)
        list = doc('option')
        for item in list.items():
            listTitle = item.text()
            listTitle = self.getStrWithUTF8(listTitle)
            # 获取目录页url
            # listUrl = item.val()
            # pageNum = int(listUrl[10:len(listUrl) - 1])
            # if pageNum < 136:
            #     print("跳过" + str(pageNum))
            #     continue
            listUrl = self.host + str(item.val())

            print("正在获取" + self.getOutputStr(listTitle) + "内容: " + self.getOutputStr(listUrl))
            self.getTitle(listUrl)

    # 获取文章标题和链接
    def getTitle(self, url):
        doc = pq(url)
        ul = doc('.chapter')
        li = ul('li')
        a = li('a')
        for item in a.items():
            # 获取文章标题
            title = item.text()
            title = self.getStrWithUTF8(title)
            # 获取文章链接
            titleUrl = self.host + item.attr('href')
            print("标题：" + self.getOutputStr(title) + "\n地址：" + self.getOutputStr(titleUrl))
            # 保存文章标题
            self.saveContent(title)
            # 根据titleUrl获取文章内容
            self.getContent(titleUrl)

    # 获取文章内容
    def getContent(self, url):
        doc = pq(url)
        content = doc('#nr1').text()
        content = self.tool.replace(content)
        content = self.getStrWithUTF8(content)
        self.saveContent(content)
        print("内容保存成功")

    # 保存标题和内容
    def saveContent(self, content):
        content = "\n" + content + "\n"
        print("保存内容类型：" + str(type(content)))
        file_name = self.dir_path + '/' + self.file_name + '.txt'
        f = open(file_name, 'a+')
        f.write(content)
        f.close()

    # 根据相对路径创建文件目录
    def mkDir(self, dir_path):
        # 去掉前后空格
        dir_path = dir_path.strip()
        # 判断路径格式是否正确
        if not dir_path.endswith('/'):
            dir_path = dir_path + '/'
        # 判断路径是否存在
        if not os.path.exists(dir_path):
            # 如果路径不存在，创建路径
            os.makedirs(dir_path)

    # 修复中文乱码
    def getStrWithUTF8(self, text):
        text = text.encode("raw_unicode_escape")
        return text

    def getOutputStr(self, text):
        try:
            text = text.decode("gbk").encode("utf-8")
        except:
            print("不能转码" + str(len(text)))
        return text

    def main(self):
        self.getAllList(self.url)


book = Book("http://m.aoyuge.com/33/33320/", "/Users/hqtech/Desktop/", "chaojiwushen2")
book.main()
