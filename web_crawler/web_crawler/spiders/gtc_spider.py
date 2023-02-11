import scrapy
from scrapy.http import Response
from scrapy.http import Request
from web_crawler.items import *
from urllib.parse import urlparse
from utils import *
import re

crawled_urls = set()  # 爬取过的 URL


class GtcSpiderSpider(scrapy.Spider):
    name = 'gtc_spider'
    allowed_domains = []
    start_urls = ['http://www.fsec.io/']
    start_domain = '.'.join(urlparse(start_urls[0]).netloc.split('.')[1:])

    def parse(self, response: Response, **kwargs):
        # print(self.allowed_domains)
        if response.status == 200:
            resp_url = response.url
            sub_domain = urlparse(resp_url).netloc
            sub_protocol = urlparse(resp_url).scheme
            if resp_url == sub_protocol + '://' + sub_domain:
                resp_url = resp_url + '/'
            url_path = urlparse(resp_url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            url_path = sub_domain + url_path[0:url_path.rfind('/')]

            html = htmlItem()
            html['filename'] = file_name
            html['os_path'] = ''.join(url_path)
            html['content'] = response.body
            html['content_type'] = response.headers['content-type']

            # print(html)
            yield html

            url_t = re.findall(r'/[a-zA-Z0-9/?=&.-]+', response.text)  # 当前网页的所有可能的链接
            for u in set(url_t):
                if self.start_domain in u:
                    # print(u)
                    add_domain(self.allowed_domains, u)

            link_urls = response.css('link::attr("href")').getall()

            for l in url_handler(url_list=link_urls, sub_protocol=sub_protocol, sub_domain=sub_domain,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path):
                yield Request(l, priority=300, callback=self.parse_link)

            pic_urls = response.css('img::attr("src")').getall()

            for p in url_handler(url_list=pic_urls, sub_protocol=sub_protocol, sub_domain=sub_domain,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path):
                yield Request(p, priority=100, callback=self.parse_pic)

            next_urls = response.css('a::attr("href")').getall()
            # print(next_urls)

            for i in url_handler(url_list=next_urls, sub_protocol=sub_protocol, sub_domain=sub_domain,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path):
                yield Request(i, priority=2)

            script_urls = response.css('script::attr("src")').getall()

            for s in url_handler(url_list=script_urls, sub_protocol=sub_protocol, sub_domain=sub_domain,
                                 start_domain=self.start_domain, crawled_urls=crawled_urls, resp_url=url_path):
                yield Request(s, priority=200, callback=self.parse_script)

        # print(len(crawled_urls))
        pass

    def parse_link(self, response: Response, **kwargs):
        if response.status == 200:
            sub_domain = urlparse(response.url).netloc
            url_path = urlparse(response.url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            url_path = sub_domain + url_path[0:url_path.rfind('/')]
            link = linkItem()

            link['filename'] = file_name
            link['os_path'] = url_path
            link['content'] = response.body
            link['content_type'] = response.headers['content-type']

            yield link
        pass

    def parse_pic(self, response: Response, **kwargs):
        if response.status == 200:
            sub_domain = urlparse(response.url).netloc
            url_path = urlparse(response.url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            url_path = sub_domain + url_path[0:url_path.rfind('/')]

            pic = picItem()

            pic['filename'] = file_name
            pic['os_path'] = url_path
            pic['content'] = response.body
            pic['content_type'] = response.headers['content-type']

            yield pic
        pass

    def parse_script(self, response: Response, **kwargs):
        if response.status == 200:
            sub_domain = urlparse(response.url).netloc
            url_path = urlparse(response.url).path
            file_name = 'index' if url_path[url_path.rfind('/') + 1:] == '' else url_path[url_path.rfind('/') + 1:]
            url_path = sub_domain + url_path[0:url_path.rfind('/')]

            script = scriptItem()

            script['filename'] = file_name
            script['os_path'] = url_path
            script['content'] = response.body
            script['content_type'] = response.headers['content-type']

            yield script
        pass
