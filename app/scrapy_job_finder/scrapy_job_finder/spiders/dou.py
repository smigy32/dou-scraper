import scrapy
from unicodedata import normalize


class DouSpider(scrapy.Spider):
    name = "dou"
    allowed_domains = ["jobs.dou.ua"]

    def start_requests(self):
        category = getattr(self, "category", None)
        additional_info = getattr(self, "additional_info", None)

        if not category and not additional_info:
            self.log("Category and additional_info is missing.")
            return

        url = f"https://jobs.dou.ua/vacancies?category={category}&search={additional_info}"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        vacancies = response.css("li.l-vacancy")
        for vacancy in vacancies:
            title = vacancy.css("a.vt::text").get()
            company_name = vacancy.css("a.company::text").get()
            yield {
                "title": normalize("NFKD", title),
                "company": normalize("NFKD", company_name),
                "link": vacancy.css("a.vt").attrib["href"],
            }
