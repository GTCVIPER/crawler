# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from web_crawler.spiders.gtc_spider import GtcSpiderSpider
from web_crawler.items import *
from urllib.parse import unquote
import os

root_path = os.getcwd() + '/results/'


class WebCrawlerPipeline:

    def web_saver(self, item, base_path):
        filename = unquote(item['filename'])
        path = unquote(item['os_path'])
        content_type = item['content_type'].decode()
        cont = item['content']
        sub_path = base_path + '/' + path
        filename = sub_path + '/' + filename
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)

        if len(unquote(item['filename']).split('.')) == 1:
            ext_name = content_type.split('=')[0].split('/')[-1].split(';')[0]
            print(content_type, ext_name)
            if ext_name == 'javascript':
                ext_name = 'js'
            filename = filename + '.' + ext_name

        print(filename)

        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(cont)
                pass

    def process_item(self, item, spider):
        os_path = root_path + GtcSpiderSpider.start_domain
        if not os.path.exists(os_path):
            os.makedirs(os_path)

            # 用 isinstance() 区分用哪个具体子类
        if isinstance(item, htmlItem):
            self.web_saver(item, os_path)
        elif isinstance(item, linkItem):
            self.web_saver(item, os_path)
        elif isinstance(item, scriptItem):
            self.web_saver(item, os_path)
        elif isinstance(item, picItem):
            self.web_saver(item, os_path)
        return item
