import scrapy

from gb_parse.loaders import HHLoader, SourceLoader
from gb_parse.spiders.xpaths import HH_PAGE_XPATH, HH_VACANCY_XPATH, HH_COMPANY_XPATH

class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113"]

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {
            "pagination": self.parse,
            "vacancy": self.vacancy_parse,
            "company": self.company_parse}

        for key, xpath in HH_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def vacancy_parse(self, response):
        loader = HHLoader(response=response)
        loader.add_value("vacancy_url", response.url)
        loader.add_value("table", "vacancy_table")
        for key, xpath in HH_VACANCY_XPATH.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()

        yield from self._get_follow_xpath(response, HH_VACANCY_XPATH[key], self.company_parse)


    def company_parse(self, response):
        loader = SourceLoader(response=response)
        loader.add_value("author_url", response.url)
        loader.add_value("table", "company_table")
        for key, xpath in HH_COMPANY_XPATH.items():
            if key == "vacancy":
                yield from self._get_follow_xpath(response, HH_COMPANY_XPATH[key], self.parse)
            else:
                loader.add_xpath(key, xpath)
        yield loader.load_item()
