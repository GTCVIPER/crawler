import scrapy
from scrapy.http import Response
from scrapy.http import Request
from web_crawler.items import *
from urllib.parse import urlparse
from urllib.parse import parse_qsl
from utils import *
import re

crawled_urls = set()  # 爬取过的 URL


class GtcSpiderSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_u = kwargs.get('url')
        self.root_u = kwargs.get('path')

    name = 'gtc_spider'
    allowed_domains = []
    start_urls = []

    start_domain = ''

    def start_requests(self):
        urls = [
            self.start_u
        ]
        self.start_urls = urls
        domain_url = urlparse(urls[0]).hostname

        # 匹配是否为 IP 地址
        ip_match = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')

        if ip_match.match(domain_url):
            self.start_domain = domain_url
        else:
            self.start_domain = '.'.join(urlparse(urls[0]).hostname.split('.')[1:])
        # self.start_domain = '.'.join(urlparse(urls[0]).netloc.split('.')[1:])
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs):
        # print(self.allowed_domains)
        if response.status == 200:
            resp_url = response.url
            sub_domain = urlparse(resp_url).hostname
            # print(type(sub_domain))
            sub_protocol = urlparse(resp_url).scheme
            if resp_url == sub_protocol + '://' + sub_domain:
                resp_url = resp_url + '/'
            url_path = urlparse(resp_url).path
            url__path = url_path
            url_params = dict(parse_qsl(urlparse(resp_url).query))
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]

            for key, value in url_params.items():
                if key in ['page', 'file', 'id', 'cat', 'product', 'category', 'blog', 'act', 'action', 'tags']:
                    if file_name == 'index':
                        url__path += key + '/'
                    else:
                        url__path += '/' + key + '/'
                    file_name = value

            port = '' if urlparse(resp_url).port == 80 or urlparse(resp_url).port is None else '/' + str(
                urlparse(resp_url).port)
            url_paths = sub_domain + port + url__path[0:url__path.rfind('/')]
            url_path_ = urlparse(resp_url).netloc + url_path[0:url_path.rfind('/')]
            # print(url_path_)

            html = htmlItem()
            html['filename'] = file_name
            html['os_path'] = ''.join(url_paths)
            html['content'] = response.body
            html['content_type'] = response.headers['content-type']

            # print(html)
            yield html

            url_t = re.findall(r'/[a-zA-Z0-9/?=&.-]+', response.text)  # 当前网页的所有可能的链接
            for u in set(url_t):
                if self.start_domain in u and u.rsplit('.')[-1] not in ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc',
                                                                        'ico', 'docx', 'ppt', 'pptx']:
                    # print(u)
                    add_domain(self.allowed_domains, u)

            link_urls = response.css('link::attr("href")').getall()

            for l in url_handler(url_list=link_urls, sub_protocol=sub_protocol, sub_domain=urlparse(resp_url).netloc,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path_):
                yield Request(l, priority=300, callback=self.parse_link)

            pic_urls = response.css('img::attr("src")').getall()

            for p in url_handler(url_list=pic_urls, sub_protocol=sub_protocol, sub_domain=urlparse(resp_url).netloc,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path_):
                yield Request(p, priority=100, callback=self.parse_pic)

            next_urls = response.css('a::attr("href")').getall()
            # print(next_urls)

            for i in url_handler(url_list=next_urls, sub_protocol=sub_protocol, sub_domain=urlparse(resp_url).netloc,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path_):
                yield Request(i, priority=2)

            script_urls = response.css('script::attr("src")').getall()

            for s in url_handler(url_list=script_urls, sub_protocol=sub_protocol, sub_domain=urlparse(resp_url).netloc,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path_):
                yield Request(s, priority=200, callback=self.parse_script)

        # print(len(crawled_urls))
        pass

    def parse_link(self, response: Response, **kwargs):
        if response.status == 200:
            sub_domain = urlparse(response.url).hostname
            url_path = urlparse(response.url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            port = '' if urlparse(response.url).port == 80 or urlparse(response.url).port is None else '/' + str(
                urlparse(response.url).port)
            url_path = sub_domain + port + url_path[0:url_path.rfind('/')]
            # url_path_ = sub_domain + url_path[0:url_path.rfind('/')]
            link = linkItem()

            link['filename'] = file_name
            link['os_path'] = url_path
            link['content'] = response.body
            link['content_type'] = response.headers['content-type']

            yield link
        pass

    def parse_pic(self, response: Response, **kwargs):
        if response.status == 200:
            sub_domain = urlparse(response.url).hostname
            url_path = urlparse(response.url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            port = '' if urlparse(response.url).port == 80 or urlparse(response.url).port is None else '/' + str(
                urlparse(response.url).port)
            url_path = sub_domain + port + url_path[0:url_path.rfind('/')]
            # url_path_ = sub_domain + url_path[0:url_path.rfind('/')]
            pic = picItem()

            pic['filename'] = file_name
            pic['os_path'] = url_path
            pic['content'] = response.body
            pic['content_type'] = response.headers['content-type']

            yield pic
        pass

    def parse_script(self, response: Response, **kwargs):
        if response.status == 200:
            sub_domain = urlparse(response.url).hostname
            url_path = urlparse(response.url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            port = '' if urlparse(response.url).port == 80 or urlparse(response.url).port is None else '/' + str(
                urlparse(response.url).port)
            url_path = sub_domain + port + url_path[0:url_path.rfind('/')]
            # url_path_ = sub_domain + url_path[0:url_path.rfind('/')]
            script = scriptItem()

            script['filename'] = file_name
            script['os_path'] = url_path
            script['content'] = response.body
            script['content_type'] = response.headers['content-type']

            yield script
        pass
