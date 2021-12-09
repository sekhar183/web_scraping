# -*- coding: utf-8 -*-
import scrapy


class CompaniesSpider(scrapy.Spider):
    name = 'companies'
    allowed_domains = ['www.3dprintingbusiness.directory/companies']
    start_urls = ['http://www.3dprintingbusiness.directory/companies/']
    page_num=1
    def parse(self, response):
        self.page_num+=1
        print(self.page_num)
        companies = response.xpath("//div[@class='listing-title']")
        for company in companies:
            name = company.xpath('.//text()').get()
            link = company.xpath('.//@href').get()

            yield{
                'company_name':name,
                'reference_link':link
            }
        print("https://www.3dprintingbusiness.directory/companies/page/{}".format(self.page_num))
        yield scrapy.Request(url="https://www.3dprintingbusiness.directory/companies/page{}".format(self.page_num), callback=self.parse, dont_filter=True)