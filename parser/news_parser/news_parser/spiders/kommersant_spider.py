import scrapy
import pandas as pd
from w3lib.html import remove_tags
import json
from ..items import Article
from ..helpers import get_date_from_text


class KommersantSpider(scrapy.Spider):
    name = "kommersant"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10000
    }

    def start_requests(self):
        start_date = '2020-10-08'
        end_date = '2021-10-01'
        dates = pd.date_range(start_date, end_date).strftime('%Y-%m-%d').to_list()
        print(dates)
        for date in dates:
            url = f"https://www.kommersant.ru/archive/rubric/3/day/{date}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'https://www.kommersant.ru'

        for link in response.css('a.uho__link::attr(href)'):
            yield scrapy.Request(url=base_url + link.get(), callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.doc_header__name::text').get().strip()
        # print(title)

        content_blocks = response.css('p.doc__text::text').getall()[:-1]
        content_blocks = [remove_tags(block).strip() for block in content_blocks]
        content = ' '.join(content_blocks)
        # print(content)

        date = response.css('time.doc_header__publish_time::text').get().split(',')[0].strip()
        date = get_date_from_text(date)
        # print(date)

        article = Article(title=title, content=content, date=date, url=response.request.url)
        yield article
