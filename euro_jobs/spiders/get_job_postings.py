# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.selector import Selector
from ..items import EuroJobsItem
import datetime
import sqlite3 as sqlite
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import sys


class EurojobspostingdetailsSpider(scrapy.Spider):
    name = 'euroJobsGetJobPostingDetails'
    allowed_domains = ['eurojobs.com']
    
    connection = sqlite.connect(settings.get('DB_PATH'))
    connection.row_factory = sqlite.Row
    cursor = connection.cursor()

    # scrape each url from urls.txt
    def start_requests(self):
           
        try:
            self.cursor.execute('SELECT * FROM joburls')
            for row in self.cursor.fetchall():
                url = row['url']
                self.cursor.execute("select * from jobdetails where url=?", (url,)) #checking for duplicate entry
                if not self.cursor.fetchone():
                    yield Request(url, self.parse)
                else:
                    print('Already Exists',url)
        except:
            print("CONNECTION WAS NOT SET")

        '''
        with open('urls.txt', 'r') as urls:
            try:
                for index, url in enumerate(urls, 1):
                    yield Request(url, self.parse)
            except:
                print("CONNECTION WAS NOT SET")
        '''

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
            salary = sel.xpath("//*[contains(text(),'Salary:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            salary = salary.strip()
        except:
            salary = ""
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
        except:
            category = ""
        try:
            jobType = sel.xpath("//*[contains(text(),'Job Category:')]/ancestor::div/div[@class='displayField']/text()").extract()[0]
            jobType = jobType.strip()
        except:
            jobType = ""
        try:
            orig_source = sel.xpath("//*[contains(text(),'Original Source')]").extract()[0]
        except:
            orig_source = ""
        try: #saving total html document
            htmlBlob = sel.xpath("//div[@class='listingInfo']/h2").extract()[0]
            htmlBlob += sel.xpath("//fieldset[@id='col-narrow-left']").extract()[0]
            htmlBlob += sel.xpath("//fieldset[@id='col-narrow-right']").extract()[0]
            htmlBlob += sel.xpath("//fieldset[@id='col-wide']").extract()[0]
            htmlBlob += sel.xpath("//div[@class='userInfo']").extract()[0]
            if orig_source: #if the html document contains a referance url then a token is set for further cleaning
                htmlBlob += htmlBlob + "<a class='Original-Source'>Original Source</a>"
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
        item['salary'] = salary


        print('item',item)
        yield item
