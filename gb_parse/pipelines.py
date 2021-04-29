# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

# from scrapy import Request
# from scrapy.pipelines.images import ImagesPipeline

from pymongo import MongoClient

mongo_client = MongoClient()

class GbParsePipeline(object):
    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database['avito_parse_22_01']
        collection.insert_one(item)
        return item

