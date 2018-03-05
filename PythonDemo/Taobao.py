#!usr/bin/python
# coding=utf-8

from pyspider.libs.base_handler import *

# 爬取开始页
PAGE_START = 1
# 爬取结束页
PAGE_END = 30
# 图片保存路径
DIR_PATH = '/var/py/mm'


class Handler(BaseHandler):
    crawl_config = {

    }

    # 初始化
    def __init__(self):
        self.base_url = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.page_num = PAGE_START
        self.total_num = PAGE_END
        self.deal = Deal()

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            print(url)
            # 爬取列表页信息
            self.crawl(url, callback=self.index_page)
            self.page_num += 1

    # 处理列表页，获取每个人的详情页地址
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.lady-name').items():
            # 爬取详情页信息
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    # 处理详情页，获取个人域名
    @config(priority=2)
    def detail_page(self, response):
        # 获取个人域名
        domain = response.doc('.mm-p-domain-info li > span').text()
        if domain:
            # 如果域名存在，拼接https
            page_url = 'https:' + domain
            # 爬取个人域名页信息
            self.crawl(page_url, callback=self.domain_page)

    # 处理域名页信息，获取姓名，个人简介，图片
    def domain_page(self, response):
        # 获取姓名
        name = response.doc('.mm-p-model-info-left-top dd > a').text()
        # 在图片保存路径中以姓名命名创建文件夹(路径)
        dir_path = self.deal.mkDir(name)
        # 获取个人简介
        brief = response.doc('.mm-aixiu-content').text()
        # 判断路径是否存在
        if dir_path:
            # 获取所有图片
            imgs = response.doc('.mm-aixiu-content img').items()
            count = 1
            # 保存简介
            self.deal.saveBrief(brief, dir_path, name)
            for img in imgs:
                # 获取图片地址
                url = img.attr.src
                if url:
                    # 获取图片扩展名
                    extension = self.deal.getExtension(url)
                    # 图片名称
                    file_name = name + str(count) + '.' + extension
                    count += 1
                    # 爬取图片
                    self.crawl(img.attr.src, callback=self.save_img,
                               save={'dir_path': dir_path, 'file_name': file_name})

    # 保存图片
    def save_img(self, response):
        # 获取图片内容
        content = response.content
        # 图片保存路径
        dir_path = response.save['dir_path']
        # 图片名称
        file_name = response.save['file_name']
        # 拼接图片完整路径
        file_path = dir_path + '/' + file_name
        # 保存图片
        self.deal.saveImg(content, file_path)


import os


# 保存图片
class Deal:

    def __init__(self):
        self.path = DIR_PATH
        # 判断路径格式是否正确
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        # 判断路径是否存在
        if not os.path.exists(self.path):
            # 路径不存在，创建路径
            os.makedirs(self.path)

    # 根据相对路径创建文件目录
    def mkDir(self, path):
        # 去掉前后空格
        path = path.strip()
        dir_path = self.path + path
        # 判断路径是否存在
        if not os.path.exists(dir_path):
            # 如果路径不存在，创建路径
            os.makedirs(dir_path)
        # 返回绝对路径
        return dir_path

    # 保存图片
    def saveImg(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    # 保存简介
    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + '/' + name + '.txt'
        f = open(file_name, 'w+')
        f.write(content)
        f.close()

    # 获取扩展名
    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension
