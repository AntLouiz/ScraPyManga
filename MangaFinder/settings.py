# -*- coding: utf-8 -*-
import getpass
from decouple import config

BOT_NAME = 'MangaFinder'

SPIDER_MODULES = ['MangaFinder.spiders']
NEWSPIDER_MODULE = 'MangaFinder.spiders'


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0)\
 Gecko/20100101 Firefox/48.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

LOG_ENABLED = config('LOG_ENABLED', default=True)
LOG_LEVEL = 'DEBUG'

ITEM_PIPELINES = {
    'MangaFinder.pipelines.ImagePipeline': 1,
}

username = getpass.getuser()
IMAGES_STORE = config(
    'IMAGES_STORE',
    default='/home/{}/PyMangá'.format(username)
)
