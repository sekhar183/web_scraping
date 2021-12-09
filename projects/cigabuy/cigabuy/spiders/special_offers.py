import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com/specials.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/specials.html', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/div"):
            if product.xpath(".//div[@class='p_box_price cf']/text()").get() is None:
                discounted_price = product.xpath(
                    ".//div[@class='p_box_price cf']/span[1]/text()").get()
                original_price = product.xpath(
                    ".//div[@class='p_box_price cf']/span[2]/text()").get()
            else:
                original_price = product.xpath(
                    ".//div[@class='p_box_price cf']/text()").get()
                discounted_price = original_price
            yield{
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url': product.xpath(".//a[@class='p_box_title']/@href").get(),
                'discounted_price': discounted_price,
                'original_price': original_price,
                'User-Agent':response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").getall()[0]

        if next_page:
           # print(next_page)
            yield scrapy.Request(url='https://www.cigabuy.com/specials.html', callback=self.parse,dont_filter=True ,headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
            })
