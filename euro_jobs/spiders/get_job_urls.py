# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request
from scrapy.selector import Selector
import pandas as pd


class EurojobsSpider(scrapy.Spider):
    name = 'euroJobsGetJobURLs'
    allowed_domains = ['eurojobs.com']
    noOfJobs = 0
    noOfPages = 0   
                
    def start_requests(self):
        
        countryJob = pd.read_csv("country-wise-job-posting.csv")
        
        for index,row in countryJob.iterrows():
            url = row['url']
            job_count = row['job_count']
            print(url,job_count)
            
            remPage = 0
            if job_count%10 > 0: remPage= 1
            pageCount = round(job_count/10)+ remPage
            print('pageCount',pageCount)
            
            i = 1
            while i <= pageCount:
                url = url+'?searchId=1606174454.9407&action=search&page='+str(i)+'&view=list'
                i = i + 1
                yield Request(url, self.parse)
        
        
            
    def parse(self, response):
        sel = Selector(response)
        # for href in sel.xpath("//div[@class='section']/ol[@class='jobs']/li[@class='job']/dl/dd[@class='title']/strong/a").extract():
        #     print("URLs are: " + href)
        f = open("urls.txt", "a")
        print('here i am')
        for href in sel.xpath("//div[@class='listing-title']/a/@href").extract():
            print('href',href)
        #for href in sel.xpath("//dl/dd[@class='title']/strong/a/@href").extract():
            f.write(href+"\n")
        f.close()
         #   print("URLs are: "+href)
        # for href in response.css('a::attr(href)'):
        #     url = response.urljoin(href.extract())
        #     print("URLs are: "+ url)
            #yield scrapy.Request(url, callback=self.print_url)

    def print_url(self, response):
        print("URLS are: "+response.url)

    # rules = (
    #     Rule(LinkExtractor(allow=(), restrict_css=('.page-numbers',)),
    #          callback="parse_item",
    #          follow=True),)

    # def parse_dir_contents(self, response):
    #     for sel in response.xpath('//ul/li'):
    #         item = DmozItem()
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item
    # def parse_item(self, response):
    #     print('Processing..' + response.url)
