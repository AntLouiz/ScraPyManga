# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class SoMangaPipeline(object):
    def process_item(self, item, spider):

        return item


class ImagePipeline(ImagesPipeline):
    
    def spider_closed(self, spider):
        print("Download finished.")
        
    def get_media_requests(self, item, info):
        
        requests = []
        
        for image_url in item.get('image_urls', []):
            requests.append(
                    Request(
                        image_url,
                        meta={
                            'image_chapter': item['image_chapter'],
                            'image_path': item['image_path'],
                            'image_name': item['image_name'],
                            'image_page': item['image_page']
                            },)
                        )
                        
        return requests
    
    def get_images(self, response, request, info):
        
        for key, image, buf, in super(ImagePipeline, self).get_images(response, request, info):
            key = self.change_filename(key, response)
            #print("Page {} downloaded.".format(response.meta['image_page']))
           
            yield key, image, buf
            
    def change_filename(self, key, response):
        return "{}/{}/{}".format(response.meta['image_path'], response.meta['image_chapter'], response.meta['image_name'])
    
    def image_downloaded(self, response, request, info):
        image = super(ImagePipeline, self).image_downloaded(response, request, info)
   
        return image
