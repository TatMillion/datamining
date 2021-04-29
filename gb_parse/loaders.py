

from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def get_parameters(item):
    selector = Selector(text=item)
    data = {
        "name": selector.xpath(
            '//span[contains(@class, "item-params-label")]/text()'
        ).extract_first(),
        "value": selector.xpath(
            '//span[contains(@class, "item-params-label")]/a/text()'
        ).extract_first(),
    }
    return data


class AvitoLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = TakeFirst()
    address_out = TakeFirst()
    author_out = TakeFirst()
    parameters_in = MapCompose(get_parameters)