# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.selector import Selector
from ..items import EuroJobsItem
import datetime


class EurojobspostingdetailsSpider(scrapy.Spider):
    name = 'euroJobsGetJobPostingDetails'
    allowed_domains = ['eurojobs.com']

    # scrape each url from urls.txt
    def start_requests(self):
        with open('urls.txt', 'r') as urls:
            try:
                for index, url in enumerate(urls, 1):
                    yield Request(url, self.parse)
            except:
                print("CONNECTION WAS NOT SET")

    # document parser
    def parse(self, response):
        expired = 0
        currentUrl = response.url
        sel=Selector(response)
        try:
            expired = sel.xpath("//*[contains(text(),'Expiry Date:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            expired = expired.strip()
        except:
            expired = ""
        try:
            title = sel.xpath("//div[@class='listingInfo']/h2/text()").extract()[0]
            title = title.strip()
        except:
            title = ""
        try:
            date = sel.xpath("//*[contains(text(),'Posted:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            date = date.strip()
        except:
            date = ""
        try:
            location = sel.xpath("//*[contains(text(),'Location:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            location = location.strip()
        except:
            location = ""
        try:
            description = sel.xpath("//*[contains(text(),'Job Description:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            description = description.strip()
        except:
            description = ""
        try:
            category = sel.xpath("//*[contains(text(),'Job Category:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            category = category.strip()
            print('category here',category)
        except:
            category = ""
        try:
            jobType = sel.xpath("//*[contains(text(),'Job Category:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            jobType = jobType.strip()
            print('jobType here',jobType)
        except:
            jobType = ""
        try:
            htmlBlob = sel.xpath("//fieldset[@id='col-wide']").extract()[0]
        except:
            htmlBlob = ""

        item = EuroJobsItem()
        item['url'] = currentUrl
        item['title'] = title
        item['date_posted'] = date
        item['category'] = category
        item['location'] = location
        item['job_type'] = jobType
        item['description'] = description
        item['html_blob'] = htmlBlob
        item['expired'] = expired

        print('item',item)
        yield item
