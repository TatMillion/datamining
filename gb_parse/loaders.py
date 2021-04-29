
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join


def flat_text(items):
    return "".join(items).replace("\xa0", "")

def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)

def description_to_list(description):
    return description.split(", ")


class HHLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()

class SourceLoader(ItemLoader):
    default_item_class = dict
    name_company = Join()
    link = Join()
    field = Join()
    description_company = MapCompose(description_to_list)
    company_vacancies = Join()