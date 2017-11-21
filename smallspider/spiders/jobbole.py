import scrapy

from scrapy.http import Request
from urllib import parse


from smallspider.items import JobBoleArticleItem, ArticleItemLoader

class JobBoleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//*[@id="archive"]/div/div[1]/a')
        for post_node in post_nodes:
            image_url = post_node.xpath('img/@src').extract_first('')
            host_url = post_node.xpath('@href').extract_first('')
            yield Request(
                 url=parse.urljoin(response.url, host_url),
                 meta={'front_image_url':image_url},
                 callback=self.parse_detail
            )
        next_page = response.xpath('//a[@class="new page-numbers"]/@href').extract_first('')
        if next_page:
            yield Request(
                url=parse.urljoin(response.url, next_page),
                callback=self.parse
            )

    def parse_detail(self, response):
        front_image_url = response.meta.get('front_image_url', '')
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('create_date', '//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_xpath('praise_nums', '//div[@class="post-adds"]/span/h10/text()')
        item_loader.add_xpath('fav_nums', '//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_xpath('content', '//div[@class="entry"]')
        article_item = item_loader.load_item()
        yield article_item
