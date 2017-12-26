# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from slugify import slugify
from MangaFinder.items import Images
from MangaFinder.settings import IMAGES_STORE
    

class ReaderSpider(scrapy.Spider):
    name = 'reader'
    
    def __init__(self, manga_data, *args, **kwargs):
        self.start_urls = ['http://somanga.net']
        self.manga_title = str(manga_data['title'])
        self.chapters = manga_data['chapters']
        self.allowed_domains = ['*']  

    def parse(self, response):
        print("Making connection with the site.")
        title = slugify(self.manga_title)

        link = 'http://somanga.net/manga/{}'.format(title)
        
        print("Searching for {}...".format(self.manga_title))

        yield scrapy.Request(
            url=link,
            callback=self.parse_detail,
            dont_filter=True,
        )

    def parse_detail(self, response):
        
        # check if the mangá is founded
        title = response.xpath(
            "//div[contains(@class, 'breadcrumbs')]/div/h1/text()"
            ).extract_first()
        
        if title:
            print("Mangá {} founded !".format(title))
        else:
            print("Mangá not found.")
            raise CloseSpider
        
        # get all chapters li's
        li_selectors = response.xpath("//ul[contains(@class, 'capitulos')]/li")
        li_selectors.reverse() # reverse the list 
        
        
        # processing the chapters 
        if len(self.chapters) == 2:
            if '-1' not in self.chapters:
                # parse str('05') to int(5)
                initial = int(self.chapters[0])-1 
                final = int(self.chapters[1])

                try:
                    range_chapters = li_selectors[initial : final]
                    
                    for chapter_li in range_chapters:
                        index = li_selectors.index(chapter_li) + 1
                        print("Downloading the Chapter {} of {}...".format(index, title))
                        chapter_link = chapter_li.xpath('./a/@href').extract_first()
                        
                        yield scrapy.Request(
                                url=chapter_link,
                                callback=self.parse_chapter,
                                meta={'title':title, 'chapter':index},
                                dont_filter=True
                                )
                except IndexError:
                    print("Chapter not found.")
            else:
                raise NotImplementedError
                    
        elif len(self.chapters) == 1: 
            
            try:
                # parse str('05') to int(5)
                initial = int(self.chapters[0])-1
                chapter_li = li_selectors[initial]
                
                chapter_link = chapter_li.xpath('./a/@href').extract_first()
                print("The download will set in the {}".format(IMAGES_STORE))

                print("Downloading the Chapter {} of {}...".format(self.chapters[0], title))

                yield scrapy.Request(
                        url=chapter_link,
                        callback=self.parse_chapter,
                        meta={'title':title, 'chapter':self.chapters[0]},
                        dont_filter=True
                )
            except IndexError:
                print("Chapter {} not found.".format(self.chapters[0]))
                 
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
