# enconding: utf-8
import re
import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from so_manga.spiders.reader import ReaderSpider


def chapters_range(string, regex = re.compile(r'(\d+)(?::(\d+))|(?::(\d+))|(\d+)(?::$)|(?::)?$')):
    """
        A type to be used to check if the chapter patterns is valid,
        return a list if the regex match.
    """
   
    if not regex.match(string):
        raise argparse.ArgumentError

    return string.split(':')


def main():
    parser = argparse.ArgumentParser(description="A test of argument parser")
    parser.add_argument('--c', type=chapters_range, action='store', nargs=1)
    parser.add_argument('--n', type=str, action='store', nargs='+')
    
    args = parser.parse_args()
    initial_chapter = args.c[0][0]
    final_chapter = args.c[0][1]
    manga_title = args.n[0]
    


    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', 
        'LOG_ENABLED': False, 
        'IMAGES_STORE': '/home/luiz/mangás',
        'ITEM_PIPELINES':{'so_manga.pipelines.ImagePipeline': 1}, })

    process.crawl(ReaderSpider, manga_title=manga_title, chapters=(initial_chapter, final_chapter))

    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
        main()
