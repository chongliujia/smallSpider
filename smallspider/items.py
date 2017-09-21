# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join




def date_convert(value):
    create_date = value.replace('.','').strip()
    return create_date

def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def return_value(value):
    return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title         = scrapy.Field()
    create_time   = scrapy.Field(
            input_processor=MapCompose(date_convert)
            )
    url           = scrapy.Field()
    url_object_id = scrapy.Field()
    font_image_url  = scrapy.Field(
            output_processor=MapCompose(return_value)
            )
    font_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
            input_processor=MapCompose(get_nums)
            )
    comment_nums = scrapy.Field(
            input_processor=MapCompose(get_nums)
            )
    fav_num     = scrapy.Field(
            input_processor=MapCompose(get_nums)
            )

    tags        = scrapy.Field(
            input_processor=MapCompose(remove_comment_tags),
            output_processor=Join(",")
            )
    content     = scrapy.Field()


