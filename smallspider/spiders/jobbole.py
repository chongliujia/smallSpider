# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from urllib import parse

from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from smallspider.items import JobBoleArticleItem, ArticleItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        self.fail_urls = []


