# enconding: utf-8

import scrapy
from scrapy.crawler import CrawlerProcess
from so_manga.spiders.reader import ReaderSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_ENABLED': False,
    'IMAGES_STORE': '/home/luizr/mangás',
    'ITEM_PIPELINES':{'so_manga.pipelines.ImagePipeline': 1},

})

process.crawl(ReaderSpider)

process.start() # the script will block here until the crawling is finished