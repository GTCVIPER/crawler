# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class htmlItem(scrapy.Item):
    filename = scrapy.Field()
    os_path = scrapy.Field()
    content = scrapy.Field()
    content_type = scrapy.Field()


class linkItem(scrapy.Item):
    filename = scrapy.Field()
    os_path = scrapy.Field()
    content = scrapy.Field()
    content_type = scrapy.Field()


class picItem(scrapy.Item):
    filename = scrapy.Field()
    os_path = scrapy.Field()
    content = scrapy.Field()
    content_type = scrapy.Field()


class scriptItem(scrapy.Item):
    filename = scrapy.Field()
    os_path = scrapy.Field()
    content = scrapy.Field()
    content_type = scrapy.Field()
