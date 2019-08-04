# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SemanticScholarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()

    img_src = scrapy.Field()

    img_num = scrapy.Field()

    citations = scrapy.Field()

    topic = scrapy.Field()

    meeting = scrapy.Field()

    pdf = scrapy.Field()

    # 如果没爬到meeting，就抓下面的信息

    venue = scrapy.Field()

    year = scrapy.Field()
