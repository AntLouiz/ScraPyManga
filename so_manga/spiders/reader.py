# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from urllib import request
from slugify import slugify
from so_manga.items import Images
from so_manga.settings import IMAGES_STORE
	

class ReaderSpider(scrapy.Spider):
    name = 'reader'
    
    def __init__(self, manga_data, *args, **kwargs):
        self.start_urls = ['http://somanga.net']
        self.manga_title = str(manga_data['manga_title'])
        self.chapters = manga_data['chapters']
        self.allowed_domains = ['*']  

    def parse(self, response):
        print("Making connection with the site.")
        title = slugify(self.manga_title)

        link = 'http://somanga.net/manga/{}'.format(title)

        yield scrapy.Request(
            url=link,
            callback=self.parse_detail,
            dont_filter=True,
        )

    def parse_detail(self, response):
        print(self.chapters)
        
        print("The download will set in the {}".format(IMAGES_STORE))

        for chapter in self.chapters:
            if chapter == '-1':
                chapter_selector = response.xpath(
                        '//div[contains(text(), "Cap ")]'
                    )
            else:
                chapter_selector = response.xpath(
                        '//div[contains(text(), "Cap {0}")]'.format(chapter)
                        )
            chapter_text = chapter_selector.xpath('./text()').extract_first()
            
            if chapter_text:

                chapter_link = chapter_selector.xpath(
                        './parent::a/@href'
                ).extract_first()
                
                title = response.xpath(
                    "//div[contains(@class, 'breadcrumbs')]/div/h1/text()"
                ).extract_first()

                yield scrapy.Request(
                    url=chapter_link,
                    callback=self.parse_chapter,
                    meta={'title':title, 'chapter':chapter_text},
                    dont_filter=True
                )
            else:
                print("Mangá not found.")
                raise CloseSpider

    def parse_chapter(self, response):
     
        imgs_urls = response.xpath(
            '//div[contains(@class, "col-sm-12 text-center")]/img/@src'
        ).extract()

        i = 0

        for img_url in imgs_urls:

    
            i += 1

            image = Images()

            image['image_urls'] = [img_url]
            image['image_path'] = response.meta['title']
            image['image_chapter'] = response.meta['chapter']
            image['image_page'] = "0"+str(i) if i < 10 else str(i)
            image['image_name'] = "{}{}".format(image['image_path'], image['image_page'])

            yield image
