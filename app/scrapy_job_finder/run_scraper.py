from .scrapy_job_finder.spiders.dou import DouSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        # The path seen from root, ie. from main.py
        settings_file_path = "app.scrapy_job_finder.scrapy_job_finder.settings"
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = DouSpider  # The spider you want to crawl

    def run_spiders(self, category, additional_info):
        self.process.crawl(self.spider, category=category, additional_info=additional_info)
        self.process.start(stop_after_crawl=True, install_signal_handlers=False)  # the script will block here until the crawling is finished
