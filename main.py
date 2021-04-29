from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from gb_parse.spiders.Hh import HhSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(HhSpider)
    crawler_proc.start()
