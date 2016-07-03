# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://voice.hupu.com/nba/2044869.html")
assert "Python" in driver.title
comment_list = driver.find_element_by_xpath('//div[@class="comment_list"]/dl')
print comment_list
assert "No results found." not in driver.page_source
driver.close()
