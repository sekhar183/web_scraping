import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com/specials.html']
    start_urls = ['https://www.cigabuy.com/specials.html']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/div"):
            if product.xpath(".//div[@class='p_box_price cf']/text()").get() is None:
                discounted_price = product.xpath(".//div[@class='p_box_price cf']/span[1]/text()").get()
                original_price = product.xpath(".//div[@class='p_box_price cf']/span[2]/text()").get()
            else:
                original_price = product.xpath(".//div[@class='p_box_price cf']/text()").get()
                discounted_price = original_price
            yield{
                'title':product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url':product.xpath(".//a[@class='p_box_title']/@href").get(),
                'discounted_price':discounted_price,
                'original_price':original_price
            }
        next_page = response.xpath("//a[@class='nextPage']/@href").getall()[0]
        if next_page:
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)