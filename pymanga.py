# enconding: utf-8
import re
import scrapy
from cli import Cli
from scrapy.utils.project import get_project_settings as settings
from scrapy.crawler import CrawlerProcess
from MangaFinder.spiders.reader import ReaderSpider

class Pymanga:
    arg_parser = Cli #set a Command Line Interface
    
    def __init__(self, *args, **kwargs):
        self.args = self.arg_parser.parse_args() #get the parser args
        self.title = self.args.name # get the value of manga title
        self.chapter = self.args.chap # get the value of manga chapters 

        self.manga_data = {
                'title': self.title,
                'chapters': self.chapter
        }

        self.spider = ReaderSpider
        self.crawler_proccess = CrawlerProcess(settings())  

    def run(self):
        self.crawler_proccess.crawl(
                self.spider,
                manga_data=self.manga_data
        )

        self.crawler_proccess.start()

def main():
    pymanga = Pymanga()
    pymanga.run()

if __name__ == "__main__":
        main()
