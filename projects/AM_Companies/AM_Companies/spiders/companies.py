# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import request


class CompaniesSpider(scrapy.Spider):
    name = 'companies'
    allowed_domains = ['www.3dprintingbusiness.directory/companies']
    start_urls = ['http://www.3dprintingbusiness.directory/companies/']
    page_num=1
    def parse(self, response):
        if self.page_num<305:
            self.page_num+=1
            print(self.page_num)
            companies = response.xpath("//div[@class='listing-title']")
            for company in companies:
                name = company.xpath('.//text()').get()
                link = company.xpath('.//@href').get()

                yield scrapy.Request(url=link, callback=self.parse_company, meta={'company_name':name,
                'link':link}, dont_filter=True)
            #print("https://www.3dprintingbusiness.directory/companies/page/{}".format(self.page_num))
            yield scrapy.Request(url="https://www.3dprintingbusiness.directory/companies/page{}".format(self.page_num), callback=self.parse, dont_filter=True)

    def parse_company(self, response):
        print("----------------------{}---------------------------".format(self.page_num))
        name = response.request.meta['company_name']
        link = response.request.meta['link']
       # print(name,link)
        info = response.xpath("//div[@class='description']/text()").getall()
        desc = response.xpath("//div[@class='block-content']/p/text()").getall()
        navi = response.xpath("//div[@class='breadcrumbs']/a/text()").getall()
        serv = response.xpath("//div[@class='range-of-services company-page-center-block']/div[@class='block-content']/ul/li/text()").getall()
        yield{
            'company_name':name,
            'reference_link':link,
            'info':info,
            'description':desc,
            'navigation':navi,
            'services':serv
            }
        