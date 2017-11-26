# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


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

class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('article_data.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
