import json
import re
from urllib.parse import urlencode, urljoin
import scrapy

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    followers = {}

    def __init__(self, login, password, persons, *args, **kwargs):
        self.persons = persons
        self.login = login
        self.password = password
        self.query_hash = 'c76146de99bb02f6415203be841dd25a'
        super().__init__(*args, *kwargs)

    def parse(self, response,  **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse_users,
                formdata={'username': self.login, 'password': self.password},
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
        )
        except AttributeError as e:
            if response.json().get('authenticated'):
                variables = {
                    'fetch_media_count': 0,
                    'fetch_suggested_count': 30,
                    'ignore_cache': True,
                    'filter_followed_friends': True,
                    'seen_ids': [],
                    'include_reel': True,

                }

                yield response.follow(
                    url=f'{self.api_url}?query_hash={self.query_hash["recommend_friends"]}&variables={json.dumps(variables)}',
                    callback=self.recommened_parse
                )

    def recommened_parse(self, response):
        variables = {
            'user_id': "",
            'include_chaining': True,
            'include_reel': True,
            'include_suggested_users': False,
            'include_logged_out_extras': False,
            'include_highlight_reels': False,
            'include_live_status': True,

        }
        rf_list = json.loads(response.text)['data']['user']['edge_suggested_users']['edges']
        for rf in rf_list:
            u_id = rf['node']['user']['id']
            variables['user_id'] = u_id

            yield response.follow(
                url=f'{self.api_url}?query_hash={self.query_hash["user"]}&variables={json.dumps(variables)}',
                callback=self.user_parse
            )

    def parse_users(self, response):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for person in self.persons:
                yield response.follow(urljoin(self.start_urls[0], person), callback=self.parse_user, cb_kwargs={'person': person})

    def parse_user(self, response, user):
        user_id = json.loads(re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % user, response.text).group()).get('id')
        user_vars = self.variables_base
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars), callback=self.parse_folowers,
                              cb_kwargs={'user_vars': user_vars, 'user': user})

    def parse_folowers(self, response, user_vars, user):
        data = json.loads(response.body)
        if self.followers.get(user):
            self.followers[user]['followers'].extend(data.get('data').get('user').get('edge_followed_by').get('edges'))
        else:
            self.followers[user] = {'followers': data.get('data').get('user').get('edge_followed_by').get('edges'),
                                    'count': data.get('data').get('user').get('edge_followed_by').get('count')}
        if data.get('data').get('user').get('edge_followed_by').get('page_info').get('has_next_page'):
            user_vars.update(
                {'after': data.get('data').get('user').get('edge_followed_by').get('page_info').get('end_cursor')})
            next_page = self.make_graphql_url(user_vars)
            yield response.follow(next_page, callback=self.parse_folowers,
                                  cb_kwargs={'user_vars': user_vars, 'user': user})


    def make_graphql_url(self, user_vars):
        result = '{url}query_hash={hash}&{variables}'.format(url=self.graphql_url, hash=self.query_hash,
                                                             variables=urlencode(user_vars))
        return result


    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace("window._sharedData =", '')[:-1])