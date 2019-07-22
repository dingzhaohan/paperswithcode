# -*- coding: utf-8 -*-
import scrapy
from github.items import GithubItem
import pandas as pd
df = pd.read_json("/home/zhaohan/Desktop/links-between-papers-and-code.json")

class GitSpider(scrapy.Spider):
    name = 'git'
    allowed_domains = ['github.com']
    start_urls = []
    for i in range(len(df)):
        start_urls.append(df["repo_url"][i])

    def parse(self, response):

        item = GithubItem()
        temp1 = response.xpath('//ul[@class="pagehead-actions"]/li/a/text()').extract()
        #print(temp[1].replace('/n','').strip(),temp[2].replace('/n','').strip(),temp[4].replace('/n','').strip(), temp[5].replace('/n','').strip(),temp[7].replace('/n','').strip(), temp[8].replace('/n','').strip())
        item["Watch"] = temp1[2].replace('/n','').replace(',','').strip().replace('"','')
        item["Star"] = temp1[5].replace('/n','').replace(',','').strip().replace('"','')
        item["Fork"] = temp1[8].replace('/n','').replace(',','').strip().replace('"','')

        temp2 = response.xpath('//div[@class="stats-switcher-wrapper"]/ul/li/a/span/text()').extract()
        item["Commit"] = temp2[0].replace('/n','').strip()
        item["Branch"] = temp2[1].replace('/n','').strip()
        item["Release"] = temp2[2].replace('/n','').strip()
        #item["Contributor"] = temp2[3].replace('/n','').strip()

        yield scrapy.Request(response.url+"/issues", meta={"item":item}, callback=self.detail_parse)


    def detail_parse(self, response):

        item = response.meta["item"]
        try:
            item["new_issue_time"] = response.xpath('//relative-time/@datetime').extract()[0]
        except:
            item["new_issue_time"] = None
        return item