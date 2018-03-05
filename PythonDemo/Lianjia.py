#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tool
import MySQLdb
import time
import urllib2
import re
import BeautifulSoup
import types

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



class Lianjia:
    '连接二手房信息'

    # 初始化
    def __init__(self):
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
        page_url = "https://bj.lianjia.com/ershoufang/pg" + str(page_num) + "ea20000bp100ep200"
        print("请求地址：" + page_url)
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
        pattern = re.compile('<div class="content.*?<div class="page-box house-lst-page-box.*?page-data=\'{"totalPage":(.*?),.*?</div>', re.S)
        match = re.search(pattern, page)
        if match:
            print "总页数为：", match.group(1).strip()
            return match.group(1)
        else:
            print self.getCurrentTime(), "获取总页码失败"
            print("页面源码：")
            print(page)
            return 0

    # 解析房屋信息
    def getHouseInfo(self, house):
        # 判断house类型
        if not type(house) is types.StringType:
            house = str(house)
        # 解析数据
        # print(house)
        pattern = re.compile('<li.*?<a.*?href="(.*?)".*?<div class="info clear.*?<div class="title.*?<a.*?>(.*?)</a>.*?<div class="address.*?<div class="houseInfo.*?<a.*?>(.*?)</a>.*?<span.*?/span>(.*?)<span.*?/span>(.*?)<span.*?/span>(.*?)<span.*?/span>(.*?)</div>.*?<div class="flood.*?<div class="positionInfo.*?>(.*?)<span.*?/span>(.*?)<span.*?<a.*?>(.*?)</a>.*?<div class="timeInfo.*?</span>(.*?)</div>.*?<div class="priceInfo.*?<div class="totalPrice.*?<span>(.*?)</span>.*?<div class="unitPrice.*?<span>(.*?)</span>', re.S)

        items = re.search(pattern, house)
        # print(items)
        if items:
            print("===========================")
            # 房屋详情连接
            houseDetailsUrl = self.tool.replace(items.group(1))
            print "房屋详情连接：", houseDetailsUrl
            # 标题
            title = self.tool.replace(items.group(2))
            print "标题：", title

            # 小区
            community = self.tool.replace(items.group(3))
            print "小区：", community
            # 户型
            houseType = self.tool.replace(items.group(4))
            print "户型：", houseType
            # 面积
            area = self.tool.replace(items.group(5))
            print "面积：", area
            # 房屋朝向
            buildingHead = self.tool.replace(items.group(6))
            print "房屋朝向：", buildingHead
            # 装修类型
            decorateType = self.tool.replace(items.group(7))
            print "装修类型：", decorateType

            # 楼层
            floor = self.tool.replace(items.group(8))
            print "楼层：", floor
            # 建筑时间
            buildingTime = self.tool.replace(items.group(9))
            print "建筑时间：", buildingTime
            # 所在区域
            location = self.tool.replace(items.group(10))
            print "所在区域：", location

            # 发布时间
            publishTime = self.tool.replace(items.group(11))
            print "发布时间：", publishTime

            # 总房价
            totalPrice = self.tool.replace(items.group(12))
            print "总房价：", totalPrice, "万"
            # 单价
            unitPrice = self.tool.replace(items.group(13))
            print "单价：", unitPrice


            question_dic = {
                "houseDetailsUrl" : houseDetailsUrl,
                "title" : title,
                "community" : community,
                "houseType" : houseType,
                "area" : area,
                "buildingHead" : buildingHead,
                "decorateType" : decorateType,
                "floor" : floor,
                "buildingTime" : buildingTime,
                "location" : location,
                "publishTime" : publishTime,
                "totalPrice" : totalPrice,
                "unitPrice" : unitPrice,
            }

            return question_dic
        else:
            return None

    # 获取某一页所有的房屋新
    def getAllHouse(self, page_num):
        # 获取页面的html
        page = self.getPageByNum(page_num)

        # 使用BeautifulSoup解析这段代码, 能够得到一个BeautifulSoup的对象
        soup = BeautifulSoup.BeautifulSoup(page)
        # 分析获得的所有问题
        houses = soup.find('div', "content")

        houses = unicode(houses)
        soup = BeautifulSoup.BeautifulSoup(houses)
        houses = soup.find('div', "leftContent")

        houses = unicode(houses)
        soup = BeautifulSoup.BeautifulSoup(houses)
        houses = soup.find('ul', "sellListContent")

        houses = unicode(houses)
        soup = BeautifulSoup.BeautifulSoup(houses)
        houses = soup.findAll('li', "clear")

        # 遍历每一个问题
        for house in houses:
            info = self.getHouseInfo(house)

            # 将获取到的问题信息保存到数据库中
            if info:
                self.mysql.insertData("lianjia_beijing_100_200", info)



lianjia = Lianjia()
# 获取总页数
total_page = int(lianjia.getTotalPageNum())

# lianjia.getAllHouse(1)

for page_num in range(1, total_page + 1):
    print("正在保存第" + str(page_num) + "页数据")
    lianjia.getAllHouse(page_num)
print("所有数据保存完成")

# lianjia.getAllHouse(17)
# lianjia.getAllHouse(33)
# lianjia.getAllHouse(41)
# lianjia.getAllHouse(98)