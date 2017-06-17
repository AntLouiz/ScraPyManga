# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from slugify import slugify
from so_manga.items import Images
import random


class ReaderSpider(scrapy.Spider):
    name = 'reader'
    allowed_domains = ['*']
    start_urls = ['http://somanga.net']

    def parse(self, response):

        titles = ["Hajime no ippo", "Shingeki no Kyojin", "Berserk", "Naruto"]
        title = slugify(random.choice(titles))

        link = 'http://somanga.net/manga/{}'.format(title)

        yield scrapy.Request(
            url=link,
            callback=self.parse_detail,
            dont_filter=True
        )

    def parse_detail(self, response):

        last_chapter_text = response.xpath(
            '//div[contains(text(), "Cap")]/text()'
        ).extract_first()

        last_chapter_link = response.xpath(
            '//ul[contains(@class, "capitulos")]/li[1]/a/@href'
        ).extract_first()

        title = response.xpath(
            "//div[contains(@class, 'breadcrumbs')]/div/h1/text()"
        ).extract_first()

        yield scrapy.Request(
            url=last_chapter_link,
            callback=self.parse_last_chapter,
            meta={'title':title, 'cap':last_chapter_text},
            dont_filter=True
        )

    def parse_last_chapter(self, response):
       
        imgs_urls = response.xpath(
            '//div[contains(@class, "col-sm-12 text-center")]/img/@src'
        ).extract()

        imgs = []
        i = 0
        for img_url in imgs_urls:
            i += 1
            image = Images()
            image['image_urls'] = [img_url]
            image['image_path'] = response.meta['title']
            image['image_cap'] = response.meta['cap']
            image['image_name'] = "{}{}".format(response.meta['title'], i)
            imgs.append(image)
        return imgs