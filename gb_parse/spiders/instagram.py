import scrapy
import json
from ..items import InstaTag, InstaPost
from datetime import datetime


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    _tag_path = "https://www.instagram.com/explore/tags/"
    _api_path = "https://www.instagram.com/graphql/query/"


    def __init__(self, login, password, tags, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response):
        try:
            js_data = self.json_data(response)
            yield scrapy.FormRequest(
                self._authorization,
                method="POST",
                callback=self.parse,
                formdata={"username": self.login, "enc_password": self.password},
                headers={"X-CSRFToken": js_data["config"]["csrf_token"]},
            )
        except AttributeError:
            for tag in self.tags:
                yield response.follow(f"{self._tag_path}{tag}/", callback=self.tag_parse)

    def json_data(self, response):
        return json.loads(
            response.xpath("//script[contains(text(), 'window._sharedData')]/text()")
                .get()
                .split("window._sharedData = ")[1][:-1]
        )

    def tag_data_parse(self, tag_data):
        item = InstaTag()
        item["date_parse"] = datetime.now()
        data = {}
        for key, value in tag_data.items():
            if not (isinstance(value, dict) or isinstance(value, list)):
                data[key] = value
        item["data"] = data
        return item

    def tag_parse(self, response):
        js_data = self.json_data(response)
        tag_data = js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]
        yield self.tag_data_parse(tag_data)
        yield from self.post_data_parse(tag_data)
        yield response.follow(self.get_api_url(tag_data), callback=self.pagination_parse)


    @staticmethod
    def post_data_parse(tag_data):
        post_data = tag_data["edge_hashtag_to_media"]["edges"]
        for edge in post_data:
            yield InstaPost(date_parse=datetime.now(), data=edge["node"])

    def pagination_parse(self, response):
        data = response.json()
        posts = data["data"]["hashtag"]
        yield from self.post_data_parse(posts)
        yield response.follow(self.get_api_url(posts), callback=self.pagination_parse)

    def get_api_url(self, tag_data):
        query_hash = "9b498c08113f1e09617a1703c22b2f32"
        variables = {
            "tag_name": tag_data["name"],
            "first": 100,
            "after": tag_data["edge_hashtag_to_media"]["page_info"]["end_cursor"],
        }
        url = f"{self._api_path}?query_hash={query_hash}&variables={json.dumps(variables)}"
        return url