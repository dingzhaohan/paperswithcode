# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from day1.items import Day1Item

class PaperswithcodeSpider(scrapy.Spider):

    name = 'paperswithcode'
    allowed_domains = ['paperswithcode.com']
    start_urls = ['https://paperswithcode.com/sota']

    def parse(self, response):
        item = Day1Item()
        se = Selector(response)
        tasklinks = se.xpath('//div[@class="sota-all-tasks"]/a/@href').extract()
        for link in tasklinks:
            new_link = "https://paperswithcode.com" + link
            #print(new_link)
            yield scrapy.Request(new_link, meta={'item': item}, callback=self.detail_parse)


    def detail_parse(self, response):
        item = response.meta['item']
        links = response.xpath('//div[@class="card"]/a/@href').extract()
        for link in links:
            new_link = "https://paperswithcode.com" + link
            #print(new_link)
            yield scrapy.Request(new_link, meta={"item": item}, callback=self.detail_parse1)


    def detail_parse1(self, response):
        item = response.meta["item"]
        number = response.xpath('//div[@class="task-followers"]/text()').extract_first()
        item["papers_with_code"] = int(number.replace(" papers with code ·", '').strip()) if number.replace(" papers with code ·", '').strip() else 0
        item["subtask"] = response.xpath('//h1[@class="task-main-title"]/text()').extract_first().strip()
        item["task"] = response.xpath('//span[@class="task-area"]/a/text()').extract_first().strip()
        n = item["papers_with_code"] // 10 + 1
        print(item["papers_with_code"], n)
        for i in range(1, n+1):
            link = "https://paperswithcode.com/task/"+item["subtask"].lower().replace(' ','-')+ ("?page=%d" % i)
            #print(link)
            yield scrapy.Request(link, meta={"item": item}, callback=self.detail_parse2)

    def detail_parse2(self, response):
        item = response.meta["item"]
        paper_detail_description_links = response.xpath('//div[@class="col-lg-9 item-content"]/h1/a/@href').extract()
        for link in paper_detail_description_links:
            link = "https://paperswithcode.com" + link
            #print(link)
            yield scrapy.Request(link, meta={"item": item}, callback=self.detail_parse3)

    # 解析第四层，获取论文详细信息
    def detail_parse3(self, response):
        item = response.meta['item']
        item["paper_title"] = response.xpath('//div[@class="paper-title"]/div/div/h1/text()').extract()
        abstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/text()').extract_first()
        hideabstract = response.xpath('//div[@class="paper-abstract"]/div/div/p/span/text()').extract()[1]
        item["paper_abstract"] = (abstract + hideabstract).replace('\n', '')
        item["repo_url"] = response.xpath('//div[@id="id_paper_implementations_collapsed"]/div/div/div/a/@href').extract()
        stars_number = response.xpath('//div[@id="id_paper_implementations_collapsed"]/div/div[@class="col-md-3"]/div/text()').extract()
        item["star_number"] = []
        for i in stars_number:
            if i.replace('\n', '').replace(' ',''):
                item["star_number"].append(i.replace('\n', '').replace(' ','').replace(',', ''))
        #print(item["star_number"])
        tags = response.xpath('//div[@class="paper-tasks"]/div/div/ul/li/a/@href').extract()
        item["task"] = []
        for tag in tags:
            tag = tag.replace('/task/', '').replace('-', ' ')
            item["task"].append(tag)
        item["paper_url_pdf"] = response.xpath('//div[@class="paper-abstract"]/div/div/a/@href').extract()[0]
        item["paper_url_abs"] = response.xpath('//div[@class="paper-abstract"]/div/div/a/@href').extract()[1]
        return item