# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoMangaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Images(scrapy.Item):

    # ... other item fields ...
    image_name = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_path = scrapy.Field()
    image_chapter = scrapy.Field()
    image_page = scrapy.Field()
