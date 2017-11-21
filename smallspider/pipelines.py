# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

from scrapy.pipelines.images import ImagesPipeline


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        try:
            if 'front_image_url' in item:
                for ok, value in results:
                    image_file_path = value['path']
                    item['front_image_path'] = image_file_path
            return item
        except Exception as e:
            print(e)
            item["front_image_path"] = '图片不可用'
            return item




class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
