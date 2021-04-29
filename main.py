from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gb_parse import settings
from gb_parse.spiders.avito import AvitoSpider


if __name__ == "__main__":
    scr_settings = Settings()
    scr_settings.setmodule("gb_parse.settings")
    proc = CrawlerProcess(settings=scr_settings)
    proc.crawl(AvitoSpider)
    proc.start()
