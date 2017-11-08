# -*- coding: utf-8 -*-
import scrapy 
import re
import datetime

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from smallspider.items import JobBoleArticleItem, ArticleItemLoader



class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
    	post_nodes = response.xpath('//*[@id="archive"]/div/div[1]/a')

    	for post_node in post_nodes:
    		image_url = post_node.xpath('img/@src').extract_first('')
    		host_url = post_node.xpath('@href').extract_first('')
    		yield Request(
    			url = parse.urljoin(response.url, host_url),
    			meta = {'front_image_url': image_url},
    			callback = self.parse_detail)
    	"""
    	#文章标题
    	title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract_first()
    	#文章创建时间
    	create_date = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract_first().strip().replace('·', '').strip()
    	#文章点赞数
    	praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first()
    	#收藏数
    	fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()

    	match_re = re.match(r'.*?(\d+).*', fav_nums)
    	if match_re:
    		fav_nums = match_re.group(1)

    	#评论数
    	comment_nums = response.xpath('//a[@href="#article-comment"]/text()').extract()[0]
    	match_re = re.match(r'.*?(\d+).*', comment_nums)
    	if match_re:
    		comment_nums = match_re.group(1)
        #文章内容
    	content = response.xpath('//div[@class="entry"]').extract()[0]

    	#标签页
    	tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
    	tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
    	tag = ','.join(tag_list)
    	"""

    def parse_detail(self,response):
    	front_image_url=response.meta.get('front_image_url','')#文章封面图，response.meta.get('front_image_url','') 前一个引号是自己定义的名称，后一个空着，这样如果就不会抛异常
    	item_loader=ArticleItemLoader(item=JobBoleArticleItem(),response=response)
    	item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
    	item_loader.add_value('url',response.url)
    	item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
    	item_loader.add_value('front_image_url',[front_image_url])
    	item_loader.add_xpath('praise_nums','//div[@class="post-adds"]/span/h10/text()')
    	item_loader.add_xpath('comment_nums','//a[@href="#article-comment"]/span/text()')
    	item_loader.add_xpath('fav_nums','//div[@class="post-adds"]/span[2]/text()')
    	item_loader.add_xpath('tags','//p[@class="entry-meta-hide-on-mobile"]/a/text()')
    	item_loader.add_xpath('content','//div[@class="entry"]')
    	article_item=item_loader.load_item()
    	yield article_item




    	"""
        '''通过item loader加载item'''
        front_image_url=response.meta.get('front_image_url','')  #文章封面图，response.meta.get('front_image_url','') 前一个引号是自己定义的名称，后一个空着，这样如果就不会抛异常
        item_loader=ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('url',response.url)
        item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('front_image_url',[front_image_url])
        item_loader.add_xpath('praise_nums','//div[@class="post-adds"]/span/h10/text()')
        item_loader.add_xpath('comment_nums','//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('fav_nums','//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_xpath('tags','//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath('content','//div[@class="entry"]')
        article_item=item_loader.load_item()
        yield article_item
        """
