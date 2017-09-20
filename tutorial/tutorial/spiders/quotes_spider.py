import scrapy

"""
1. 使用以下命令
    scrapy crawl quotes
执行这个spider

2.  用scrapy shell进入测试模式
    scrapy shell "http://quotes.toscrape.com/page/1/"
    
    获取到title对象
    response.css('title')

    获取到title的文字对象，并提取出文字.
    response.css('title::text').extract()
    
    由于extract()返回的是一个list,如果确实只需要第一个元素使用extract_first()
    response.css('title::text').extract_first()
    response.css('title::text')[0].extract() #可能会产生越界访问，为了使代码能够应付错误的情况最好使用上面的格式
    
    除了使用extract()以外，还可以使用re()利用正则进行匹配
    response.css('title::text').re(r'Quotes.*')
    response.css('title::text').re(r"Q\w+')
    
    如何正则中不存在()也就是不使用group,那么返回的结果包含正则表达式可以匹配上的所有字符
    如果使用了group, 那么只捕获group的内容
    response.css('title::text').re(r'(\w+) to (\w+)')
    
    
    
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
    # 利用css selector提取出我们需要的字段
    # 一个spider typically generates many dictionaryies containing the data extracted from the page
    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags a.tag::text").extract()
            }

# 如何输出到文件，以json格式输出
# scrapy crawl quotes -o quotes.json

# 如何以json lines格式输出, JL格式把一个record处理成一行，方便后续的流处理
# scrapy crawl quotes -o quotes.jl
