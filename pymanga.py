# enconding: utf-8
import re
import scrapy
from cli import Cli
from scrapy.utils.project import get_project_settings as settings
from scrapy.crawler import CrawlerProcess
from MangaFinder.spiders.reader import ReaderSpider

class MangaDataField(dict):
    """
        A descriptor to validate the chapters and manga title
    """ 
    def __setitem__(self, key, value): 
        if key == 'chapters':
            if isinstance(value, (list, tuple,)):
                chapters = []
                chapters.append(value[0])
                if len(value) > 1:
                    chapters.append(value[1])

                dict.__setitem__(self, key, chapters)

        elif key == 'title':
            value = "".join(value)
            
            dict.__setitem__(self, key, value)
        else:
            raise Exception #change this exception later

class Pymanga:
    arg_parser = Cli #set a Command Line Interface
    
    def __init__(self, *args, **kwargs):
        self.args = self.arg_parser.parse_args() #get the parser args
        self.title = self.args.n # get the value of manga title
        self.chapters = self.args.c[0] # get the value of manga chapters 

        self.manga_data = MangaDataField(
                title=self.title,
                chapters=self.chapters
        )

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
