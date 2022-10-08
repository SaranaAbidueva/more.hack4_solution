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
        end_date = '2022-10-08'
        dates = pd.date_range(start_date, end_date).to_list
        print(dates)
        url = f'https://api.forbes.ru/api/pub/lists/biznes?list%5Blimit%5D={limit}&list%5Boffset%5D={offset}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'https://www.forbes.ru/'

        data = json.loads(response.text)

        for link in data['articles']:
            yield scrapy.Request(url=base_url + link['data']['url_alias'], callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        # print(title)

        content_blocks = response.css('p.yl27R span::text').getall()
        content_blocks = [remove_tags(block).strip() for block in content_blocks]
        content = ' '.join(content_blocks)

        date = response.css('time::text').get().replace('г.', '').strip()
        date = get_date_from_text(date)

        article = Article(title=title, content=content, date=date)
        yield article
