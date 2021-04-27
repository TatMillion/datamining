import scrapy
from base64 import b64decode

import pymongo

class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['http://auto.youla.ru/']

    _css_selectors = {
        "brands": ".TransportMainFilters_brandsList__2tIkv .ColumnItemList_container__5gTrc a.blackLink",
        'pagination': "a.Paginator_button__u1e7D",
        "car": ".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu",
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.db_client["gd_data_mining_youla"]

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, self._css_selectors["brands"], self.brand_parse)


    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors["pagination"], self.brand_parse)

        yield from self._get_follow(response, self._css_selectors["car"], self.car_parse)

    def car_parse(self, response):
        data = {}
        for key, funk in self._get_data_template().items():
            try:
                data[key] = funk(response)
            except (ValueError, AttributeError) as ex:
                print(ex)
        self.db[self.name].insert_one(data)

    def _get_data_template(self):
        return {
            "title": lambda resp: resp.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),

            "image": lambda resp: resp.css(
                "figure.PhotoGallery_photo__36e_r img::attr(src)"
            ).extract(),
            "price": lambda resp: float(resp.css('div.AdvertCard_price__3dDCr::text').get().replace("\u2009", '')),
            "characteristics": lambda resp: [
                {
                    "name": itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
                    "value": itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first()
                             or itm.css(".AdvertSpecs_data__xK2Qx a::text").extract_first(),
                }
                for itm in resp.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")
            ],
            "description": lambda resp: resp.css("div.AdvertCard_descriptionInner__KnuRi::text").get(),

            "author": lambda resp: self._get_author_id(resp).get("author"),
            "phone": lambda resp: self._get_author_id(resp).get("phone"),
        }


    @staticmethod
    def _get_author_id(response):
        data = {}
        for script in response.css("script::text").extract():
            marker = "window.transitState = decodeURIComponent"
            if marker in script:

                start = script.rfind("youlaId%22%2C%22") + 16
                end = script.find("%22%2C%22avatar")
                if end == -1:
                    end = script.find("%22%2C%22alias")
                data["author"] = response.urljoin(f"/user/{script[start:end]}").replace("auto.", "", 1)

                start = script.find("phone%22%2C%22") + 14
                end = script.find("%3D%3D%22%2C%22")
                data["phone"] = b64decode(b64decode(f"{script[start:end]}==")).decode("utf-8")
        return data
