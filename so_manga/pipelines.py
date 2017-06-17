# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import string
from scrapy.http import Request
import random
from scrapy.pipelines.images import ImagesPipeline


class SoMangaPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		requests = []

		for image_url in item.get('image_urls', []):
			requests.append(
				Request(
					image_url,
					meta={
						'image_cap': item['image_cap'],
						'image_path': item['image_path'],
						'image_name': item['image_name']
					}
				)
			)

		return requests

	def get_images(self, response, request, info):

		for key, image, buf, in super(ImagePipeline, self).get_images(response, request, info):
			
			key = self.change_filename(key, response)
			yield key, image, buf

	def change_filename(self, key, response):
		return "{}/{}/{}.jpg".format(response.meta['image_path'], response.meta['image_cap'], response.meta['image_name'])