# enconding: utf-8
import re
import scrapy
from cli import Cli
from scrapy.utils.project import get_project_settings as settings
from scrapy.crawler import CrawlerProcess
from MangaFinder.spiders.reader import ReaderSpider

class Pymanga:

    def __init__(self, title=None, chapter=None):
        if not isinstance(title, str):
            msg = "title argument must be str."
            raise ValueError(msg)

        elif not isinstance(chapter, int):
            msg = "chapter argument must be int."
            raise ValueError(msg)

        self.title = title
        self.chapter = chapter

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
    arg_parser = Cli #set a Command Line Interface
    args = arg_parser.parse_args() #get the parser args

    pymanga = Pymanga(" ".join(args.name), args.chap[0])
    pymanga.run()

if __name__ == "__main__":
        main()
