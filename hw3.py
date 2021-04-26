
import requests
import bs4
import datetime as dt
from urllib.parse import urljoin
from database.database import Database



class GbBlogParse:

    def __init__(self, start_url, database: Database):
        self.db = database
        self.start_url = start_url
        self.done_urls = set()
        self.tasks = [
            self.get_task(self.start_url, self.parse_feed),
        ]
        self.done_urls.add(self.start_url)

    def get_task(self, url, callback):
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        return task

    def _get_response(self, url):
        response = requests.get(url)
        return response

    def _get_soup(self, url):
        soup = bs4.BeautifulSoup(self._get_response(url).text, "lxml")
        return soup

    def parse_post(self, url, soup):
        post_id = soup.find('comments').attrs.get('commentable-id')
        author_tag = soup.find('div', attrs={'itemprop': 'author'})
        author_href = author_tag.parent.attrs.get("href")
        author_id_pos = author_href.rfind("/") + 1
        publish_date = soup.find('time', attrs={'itemprop': 'datePublished'})

        data = {
            'post_data': {
                'id': post_id,
                'title': soup.find('h1', attrs={'class': 'blogpost-title'}).text,
                'url': url,
                'image': soup.find('div', attrs={'class': 'hidden', 'itemprop': 'image'}).text,
                'publication_date': dt.datetime.fromisoformat(publish_date.attrs.get('datetime')),
            },
            'author_data': {
                'id': author_href[author_id_pos:],
                'url': urljoin(url, author_tag.parent.attrs.get("href")),
                'name': author_tag.text,
            },
            'tags_data': [
                {'name': tag.text, 'url': urljoin(url, tag.attrs.get('href'))}
                for tag in soup.find_all('a', attrs={'class': 'small'})
            ],
            'comments_data': self._get_comments(post_id),
        }
        return data

    def _get_comments(self, post_id):
        api_path = f'/api/v2/comments?commentable_type=Post&commentable_id={post_id}&order=desc'
        response = self._get_response(urljoin(self.start_url, api_path))
        data = response.json()
        return data

    def parse_feed(self, url, soup):
        ul = soup.find('ul', attrs={'class': 'gb__pagination'})
        pag_urls = set(
            urljoin(url, href.attrs.get('href'))
            for href in ul.find_all('a')
            if href.attrs.get('href')
        )
        for pag_url in pag_urls:
            if pag_url not in self.done_urls:
                self.tasks.append(self.get_task(pag_url, self.parse_feed))
                self.done_urls.add(pag_url)
        post_items = soup.find('div', attrs={'class': 'post-items-wrapper'})
        posts_urls = set(
            urljoin(url, href.attrs.get('href'))
            for href in post_items.find_all('a', attrs={'class': 'post-item__title'})
            if href.attrs.get('href')
        )
        for post_url in posts_urls:
            if post_url not in self.done_urls:
                self.tasks.append(self.get_task(post_url, self.parse_post))
                self.done_urls.add(post_url)

    def run(self):
        for task in self.tasks:
            task_result = task()
            if task_result:
                self.save(task_result)

    def save(self, data):
        self.db.create_post(data)


if __name__ == '__main__':
    database = Database('sqlite:///gb_blog_posts.db')
    parser = GbBlogParse('https://gb.ru/posts/', database)
    parser.run()