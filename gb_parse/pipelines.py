# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
import pymongo


class GbParsePipeline:
    def process_item(self, item, spider):
        return item


class GbParseMongoPipeline:
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client["gb_parse_hh"]

    def process_item(self, item, spider):
        table = item["table"][0]
        self.db[table].insert_one(item)
        return item