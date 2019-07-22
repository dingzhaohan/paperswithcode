# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Watch = scrapy.Field()

    Star = scrapy.Field()

    Fork = scrapy.Field()

    Commit = scrapy.Field()

    Branch = scrapy.Field()

    Release = scrapy.Field()

    Contributor = scrapy.Field()

    new_issue_time = scrapy.Field()