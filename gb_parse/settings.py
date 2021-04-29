# Scrapy settings for gb_parse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'gb_parse'

SPIDER_MODULES = ['gb_parse.spiders']
NEWSPIDER_MODULE = 'gb_parse.spiders'

LOG_ENABLE = True
LOG_LEVEL = 'DEBUG'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-reguests': '1',
    'cookie': 'u=2onwxm7v.1d1kigv.ddybhhtjza00; buyer_location_id=633540; __cfduid=d718728b23e193ba807bf3577cd81a8dd1618669500; _ym_uid=1618669503257983083; _ym_d=1618669503; _gcl_au=1.1.373695777.1618669504; _ga=GA1.2.1072834442.1618669504; _gid=GA1.2.2142454643.1618669504; _fbp=fb.1.1618669504334.856213832; luri=krasnodar; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRUlCSk1vdE8zdlNBMlpOTmNUZENybmNxbVdGclI1bnhMdUFHRkZBd3djeU52TTUxVEtkcXExYkwxSHRReXUwWFdxbEtlUk9zYXZiVG5rdjJ0U2gzeEtDVGswcGhFUjdmQ0NkMzFkOVU4Nm5GZE44VzhvdE1iMWdabFd4RnA4OTNBZHBvbmVIcE5HMG9UOTlqOFZGeGpnRUdEeVV3a2dMaTlmSjUxbDNTcjZOU2dWTktUY0Fsb2NOQUFMTlJ2VXduV3YrOWNmRjB0RGoyRm9pSFhyRENEaTAzbDlkWmtBc0VLSlBtM1premF0K2dWRDhFMStlbUJVN1lSZ3EyK3drM1ciLCJpYXQiOjE2MTg2Njk1MDIsImV4cCI6MTYxOTg3OTEwMn0.h_sirj9Sq1ZnVz4k2J16FalwIsQkRvjn3-688l5cnCQ; f=5.075fb8b9995e92ff36b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9e2bfa4611aac769efa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da7be2fce6256b648cdde01905e00c6523f2985db2d99140e2d0ee226f11256b780315536c94b3e90e338f0f5e6e0d2832e148af97ce8307cffa606506660fbbb5346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f215cd9b8add63c90ef2da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="m//BVv6kSdn+m6bYDo0pVo7JYFNH4d+o1FdlvtfXxtNSkKjK+aw2U37g8sRz/J1HoV/C2KL9r/KBgp9emMDnXqArGErM4kcuUORAwhAxK6Y0FF+oBHvH7To+A1P3BdGRBT9LdFuca84fkBMDjLFGw4guZ/NoLymAHSEM9ni1RODQRlZhRLKzzbkOSeuo/HEW"; v=1618844610; sx=H4sIAAAAAAACA1XQQXbCQAiA4bvM2gUTSYLeZsoY0tKUVyeGJj7v3nGhtXvexw/XQFvWQS/TClJYAM3dChWmcLyGJRyDxi3P0/yRiigDsRMW4jrjgkYQduEUjrGLdNhHiHDbhdzzNqbT1jmoMakRihQr9iTx5zyva5/3COAKbmJmrATO4P5HEraR+ko2/bh8T+0yxVS9Oisi5ATyIKfL1/ltgPc8KCBibTVHL4IC7CIvZIt931ayr2UFMnZjLSBQFhMAEn6QqUk0bqnNDTAUtCqSqrCKIxG9kgT7w70SY4pjN8x08Lq2aGFjdHke3uBCXZckTZ+sYEoGguj3PyGQ/SNjQ7fbL4fKeFagAQAA; so=1618844610; dfp_group=20; SEARCH_HISTORY_IDS=1; no-ssr=1; _ym_visorc=b; _ym_isad=2; buyer_from_page=catalog'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'gb_parse.middlewares.GbParseSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    # 'gb_parse.middlewares.GbParseDownloaderMiddleware': 543,
#    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
#    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html



ITEM_PIPELINES = {
   'gb_parse.pipelines.GbParsePipeline': 300,
   # 'gb_parse.pipelines.GbParseMongoPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html

# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# AUTOTHROTTLE_START_DELAY = 3
# # The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# #AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ROTATING_PROXY_LIST_PATH = (
#     "D:/"
# )
#
