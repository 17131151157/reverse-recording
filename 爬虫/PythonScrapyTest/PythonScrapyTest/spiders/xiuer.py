import scrapy


class XiuerSpider(scrapy.Spider):
    name = "xiuer"
    allowed_domains = ["xiuer.pro"]
    start_urls = ["https://xiuer.pro"]

    def parse(self, response):
        pass
