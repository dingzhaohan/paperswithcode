# -*- coding: utf-8 -*-
import scrapy
from semantic_scholar.items import SemanticScholarItem
import pandas as pd

df1 = pd.read_json('/Users/zhaohan/Desktop/links-between-papers-and-code.json')
#df2 = pd.read_json('/Users/zhaohan/Desktop/papers-with-abstracts.json')


class LittleSSpider(scrapy.Spider):
    name = 'little_s'
    allowed_domains = ['semanticscholar.org']
    start_urls = []

    for i in range(len(df1)):
        arXiv_id = df1["paper_arxiv_id"][i]
        if arXiv_id:
            start_urls.append("https://api.semanticscholar.org/arXiv:" + arXiv_id)

    def parse(self, response):

        item = SemanticScholarItem()

        img_src = response.xpath('//ul[@class="flex-row paper-detail-figures-list"]/li/a/@href').extract()

        item["img_src"] = []

        for i in img_src:
            item["img_src"].append("https://www.semanticscholar.org" + i)

        item["img_num"] = len(item["img_src"])

        item["title"] = response.xpath('//h1/text()').extract()

        item["citations"] = response.xpath('//span[@class="scorecard__description__number"]/text()').extract()

        item["topic"] = response.xpath('//span[@class="preview-box__target"]/a/text()').extract()

        item["meeting"] = response.xpath('//a[@class="doi__link"]/text()').extract()

        item["pdf"] = response.xpath('//a[@data-selenium-selector="paper-link"]/@href').extract()

        if not item["meeting"]:

            item["venue"] = response.xpath('//span[@data-selenium-selector="venue-metadata"]/span/span/text()').extract()
            item["year"] = response.xpath('//span[@data-selenium-selector="paper-year"]/span/span/text()').extract()

        yield item