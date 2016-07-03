# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# class HupuItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class HupPage(Item):
    page_url = Field() # url
    title = Field() # title (question)
    content = Field() # optional (for bbs, no content)
    post_user = Field()

class HupComment(Item):
    page_url = Field()
    comment = Field()
    comment_user_name = Field()
    comment_user_id = Field()
    floor = Field()
    quote_floor = Field()
    score = Field()
