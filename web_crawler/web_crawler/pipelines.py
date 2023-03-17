# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from web_crawler.items import *
from urllib.parse import unquote
import os
import re
from proj_path import path_

root_path = path_ + '/uploads'


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

        # print(filename)

        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(cont)
                pass

    def process_item(self, item, spider):
        global root_path
        # print(spider.start_domain, '==============>')
        # root_path = root_path + '/' + spider.root_u
        ip_match = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if not spider.root_u in root_path:
            root_path = root_path + '/' + spider.root_u
        if ip_match.match(spider.start_domain):
            os_path = root_path
        else:
            os_path = root_path + '/' + spider.start_domain
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
