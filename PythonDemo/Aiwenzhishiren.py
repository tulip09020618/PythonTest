#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tool
import MySQLdb
import time
import urllib2
import re
import BeautifulSoup
import types

class Page:

    def __init__(self):
        self.tool = Tool.Tool()


class Mysql:
    '数据库操作'

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 初始化数据库
    def __init__(self):
        try:
            self.db = MySQLdb.connect('localhost', 'root', 'jinrui0902', 'test')
            self.cur = self.db.cursor()
            print("数据库连接成功")
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])

    # 插入数据
    def insertData(self, table, my_dict):
        try:
            self.db.set_character_set('utf8')
            cols = ','.join(my_dict.keys())
            values =  '","'.join(my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return  insert_id
                else:
                    return 0
            except MySQLdb.Error, e:
                # 发生错误时回滚
                self.db.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print self.getCurrentTime(), "数据已存在，未插入数据"
                else:
                    print self.getCurrentTime(), "插入数据失败，原因%d：%s" % (e.args[0], e.args[1])
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "插入数据失败，原因%d：%s" % (e.args[0], e.args[1])


class Aiwenzhishiren:
    '爱问知识人'

    # 初始化
    def __init__(self):
        self.page_num = 1
        self.total_num = None
        self.page_spider = Page()
        self.mysql = Mysql()
        self.tool = Tool.Tool()

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 获取某一页的URL
    def getPageUrlByNum(self, page_num):
        page_url = "https://iask.sina.com.cn/search?searchWord=Python&page=" + str(page_num)
        return page_url

    # 获取某一页面的HTML
    def getPageByNum(self, page_num):
        request = urllib2.Request(self.getPageUrlByNum(page_num))
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print self.getCurrentTime(), "获取页面失败，错误代号", e.code
                return None
            if hasattr(e, "reason"):
                print self.getCurrentTime(), "获取页面失败，原因", e.reason
                return None
        else:
            page = response.read().decode('utf-8')
            return page

    # 获取总页数
    def getTotalPageNum(self):
        print self.getCurrentTime(), "正在获取目录页面个数，请稍候"
        page = self.getPageByNum(1)
        # 匹配页码总数
        pattern = re.compile('<div class="pw.*?<div class="page.*?pageCount="(.*?)".*?</div>', re.S)
        match = re.search(pattern, page)
        if match:
            print "总页数为：", match.group(1).strip()
            return match.group(1)
        else:
            print self.getCurrentTime(), "获取总页码失败"
            print("页面源码：")
            print(page)
            return 0

    # 分析问题代码，得到问题，回答，标签，时间，回答者，回答个数
    def getQuestionInfo(self, question):
        # 判断question类型
        if not type(question) is types.StringType:
            question = str(question)
        # 解析数据
        # print(question)
        pattern = re.compile('<p.*?<a.*?>(.*?)</a>.*?<p.*?>(.*?)</p>.*?<p.*?<span.*?<a.*?>(.*?)</a>.*?<span.*?>(.*?)</span>.*?<span.*?<a.*?>(.*?)</a>.*?<span.*?<a.*?>(.*?)</a>', re.S)
        items = re.search(pattern, question)
        # print(items)
        if items:
            print("===========================")
            # 问题标题
            title = self.tool.replace(items.group(1))
            print "问题：", title
            # 回答内容
            content = self.tool.replace(items.group(2))
            print "回答：", content
            # 标签
            tag = self.tool.replace(items.group(3))
            print "标签：", tag
            # 时间
            questionTime = self.tool.replace(items.group(4))
            print "时间：", questionTime
            # 回答者
            answer = self.tool.replace(items.group(5))
            print "回答者：", answer
            # 回答数
            count = self.tool.replace(items.group(6))
            print "回答数：", count

            question_dic = {
                "question" : title,
                "content" : content,
                "tag" : tag,
                "questionTime" : questionTime,
                "answer" : answer,
                "answerCount" : count
            }

            return question_dic
        else:
            return None

    def getQuestion(self, page_num):
        # 获取页面的html
        page = self.getPageByNum(page_num)

        # 使用BeautifulSoup解析这段代码, 能够得到一个BeautifulSoup的对象
        soup = BeautifulSoup.BeautifulSoup(page)
        # 分析获得的所有问题
        questions = soup.find('div', "search-list")

        questions = unicode(questions)
        soup = BeautifulSoup.BeautifulSoup(questions)
        questions = soup.find('ul')

        questions = unicode(questions)
        soup = BeautifulSoup.BeautifulSoup(questions)
        questions = soup.findAll('li')

        # 遍历每一个问题
        for question in questions:
            info = self.getQuestionInfo(question)
            # 将获取到的问题信息保存到数据库中

            if info:
                self.mysql.insertData("aiwenzhishiren", info)




aiwen = Aiwenzhishiren()
# 获取总页数
total_page = int(aiwen.getTotalPageNum())
for page_num in range(1, total_page + 1):
    print("正在保存第" + str(page_num) + "页数据")
    aiwen.getQuestion(page_num)
print("所有数据保存完成")
