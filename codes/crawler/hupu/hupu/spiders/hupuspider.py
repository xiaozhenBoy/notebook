# -*- coding: utf-8 -*-

import re
import datetime
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from hupu.items import HupPage, HupComment

from scrapy.linkextractors import LinkExtractor

comment_jsons_re = "var json\_all\_replies = eval\(\[.*?\]\);"

class HupuSpider(CrawlSpider):
    name = "HupuSpider"
    allow_domain = ['voice.hupu.com']
    start_urls = [
        "http://voice.hupu.com/nba/2044869.html"
    ]
    # "http://bbs.hupu.com/all-nba", "http://nba.hupu.com/" "http://voice.hupu.com/soccer/2044794.html"
    #
    def parse(self, response):
        """
        parse normal hupu page,
        parse http://voice.hupu.com/nba/2044869.html
        """
        curl = response.url
        sel = Selector(response)
        # get hupPage
        hp = HupPage()
        hp['title'] = sel.xpath('//div[@class="artical-title"]/h1/text()').extract()
        hp['content'] = sel.xpath('//div[@class="artical-main-content"]/*/text()').extract()
        hp['page_url'] = curl
        hp['post_user'] = ''
        yield hp
        # get comments
        comments = self.getComments(response, curl)
        #for c in comments:
        #    yield c

    def getComments(self, se_response, curl):
        # get comments
        html_body = se_response.body
        m = re.search(comment_jsons_re, html_body)
        if m:
            comment_jsons = m.groups()[0]
        else:
            comment_jsons = None
        fout = open('temp.txt', 'w')
        fout.write(comment_jsons)
        fout.close()
        return None
        # *************************************************************#
        # comment_list = se_response.xpath('//div[@class="comment_list"]/dl')
        # print "Comments:", len(comment_list)
        # comments = []
        # for c in comment_list:
        #     hc = HupComment()
        #     hc['page_url'] = curl
        #     hc['comment_user_name'] = c.xpath('@data-uname').extract()
        #     hc['comment_user_id'] = c.xpath('@data-uid').extract()
        #     hc['floor'] = c.xpath('@data-floor').extract()
        #     hc['comment'] = c.xpath('//dt[class="comm-dd"]/div[class="J_reply_content"]/text()').extract()
        #     try:
        #         hc['quote_floor'] = c.xpath('//dt[class="comm-dd"]/div[class="reply-quote-text"]/div[class="reply-quote-hd"]/text()').extract()
        #     except:
        #         pass # null reply floor
        #     comments.append(hc)
        # return comments
