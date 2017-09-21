# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        article_nodes = response.css('div#archive .floated-thumb .post-thumb a')
        for article_node in article_nodes:
            font_image_url = article_node.css('img::attr(src)').extract_first("")
            article_url = article_node.css('::attr(href)').extract_first("")

            yield Request(url=parse.urljoin(response.url, article_url), meta={
                'font_image_url':parse.urljoin(response.url, font_image_url)
            }, callback=self.parse_detail)

            next_url = response.css('a.next.page-numbers::attr(href)').extract_first("")
            if next_url:
                yield Request(url=parse.urljoin(response.url, next_url),callback=self.parse)





    def parse_detail(self, response):
        title = response.xpath('//div[@class=entry-header"]/h1/text()').extract_first()
        create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().replace('.','').strip()
        up_num = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first()
        fav_num = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()

        match_re = re.match('.*?(\d+).*', fav_num)

        if match_re:
            fav_num = match_re.group(1)
        else:
            fav_num = 0

        comment_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        match_re = re.match('.*?(\d+).*', comment_num)

        if match_re:
            comment_num = match_re.group(1)
        else:
            comment_num = 0

        content = response.xpath('//div[@class="entry-header"]').extract_first()

        tags_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract_first()
        tags_list = [element for element in tags_list if not element.strip().endswitch('评论')]
        tags = ",".join(tags_list)