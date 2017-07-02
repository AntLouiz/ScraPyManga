# enconding: utf-8
import re
import argparse
import scrapy
from scrapy.utils.project import get_project_settings as settings
from scrapy.crawler import CrawlerProcess
from so_manga.spiders.reader import ReaderSpider

def chapters_range(string, regex = re.compile(r'(\d+)(?::(\d+))|(^$::(\d+))|(\d+)(::^$)|(^:$)|(\d+)')):
    """
        A type to be used to check if the chapter patterns is valid,
        return a list if the regex match.
    """
   
    if not regex.match(string):
        raise argparse.ArgumentError

    string = string.split(':')
    
    # validations of chapters range
    
    for chapter in string:
        # change a unknown chapter to the value  -1 
        if chapter == '':
            index = string.index(chapter)
            string[index] = '-1'
            
    if len(string) == 2:
        # if the chapters range have two numbers and not of them is a unknown chapter,
        # test if first chapter on the range is higher than second.
        
        if int(string[0]) > int(string[1]) and '-1' not in string:
            raise argparse.ArgumentError

    for chapter in string:
        if int(chapter) < 10 and chapter != '-1': 
            index = string.index(chapter) 
            string[index] = '0' + chapter
    
    return string


def main():
    parser = argparse.ArgumentParser(description="A test of argument parser")
    parser.add_argument('--c', type=chapters_range, action='store', nargs=1)
    parser.add_argument('--n', type=str, action='store', nargs='+')
    
    args = parser.parse_args()
    manga_data = {
            'manga_title': None,
            'chapters': []
            }
    
    manga_data['chapters'].append(args.c[0][0])
 
    if len(args.c[0]) == 2:
        manga_data['chapters'].append(args.c[0][1])
     
    manga_data['manga_title'] = " ".join(args.n)

    process = CrawlerProcess(settings())

    process.crawl(ReaderSpider, manga_data=manga_data)

    process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
        main()
