import scrapy

"""
使用以下
    scrapy crawl quotes
执行这个spider
"""

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    # 需要返回一个request的列表 或者把start_request做成一个generator
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1',
            'http://quotes.toscrape.com/page/2',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # scrapyRequest发出以后得到的response。parse是对response的回调函数
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)