# Источник: https://5ka.ru/special_offers/
#
# Задача организовать сбор данных,
# необходимо иметь метод сохранения данных в .json файлы
#
# результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются в Json вайлы, для каждой категории товаров должен быть создан отдельный файл и содержать товары исключительно соответсвующие данной категории.
#
# пример структуры данных для файла:
# нейминг ключей можно делать отличным от примера
#
# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }


import time
import json
from pathlib import Path
import requests


class Parse5ka:
    headers = {"User-Agent": "Maxim Galkin"}

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(1)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url: str):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


class CategoriesParser(Parse5ka):
    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self):
        return requests.get(self.categories_url).json()

    def run(self):
        for category in self._get_categories():
            url_product = f'{self.start_url}?categories={category["parent_group_code"]}'
            category['products'] = list(self._parse(url_product))
            file_name = f"{category['parent_group_code']}.json"
            path_to_file = self.save_path.joinpath(file_name)
            self._save(category, path_to_file)


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    save_path_products = get_save_path("products")
    save_path_categories = get_save_path("categories")
    parser_products = Parse5ka(url, save_path_products)
    cat_parser = CategoriesParser(cat_url, url, save_path_categories)
    cat_parser.run()

print('end')