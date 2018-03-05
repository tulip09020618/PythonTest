#!usr/bin/python
# -*- coding : utf-8 -*-

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 继承unittest.TestCase，表明这是一个测试类
class PythonOrgSearch(unittest.TestCase):
    '测试用例'

    # 初始化方法，这个方法会在每个测试类中自动调用
    def setUp(self):
        self.driver = webdriver.Chrome()

    # 每一个测试方法命名都有规范，必须以 test 开头，会自动执行
    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        # 找到页面中的元素
        elem = driver.find_element_by_name("q")
        # 输入内容
        elem.send_keys("pycon")
        # 模拟点击回车按键
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    #  tearDown 方法会在每一个测试方法结束之后调用。这相当于最后的析构方法
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main


