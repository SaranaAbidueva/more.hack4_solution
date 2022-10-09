import scrapy
from w3lib.html import remove_tags
from ..items import Article
import re
from ..helpers import get_date_from_text


class ConsultantSpider(scrapy.Spider):
    name = "consultant"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 50000
    }

    def start_requests(self):
        url = 'http://www.consultant.ru/legalnews/buh/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'http://www.consultant.ru'
        for link in response.css('a.listing-news__item-title::attr(href)'):
            yield scrapy.Request(url=base_url + link.get(), callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.news-page__title::text').get()

        content_blocks = response.css('div.news-page__text p').getall()
        content_blocks = [remove_tags(block).strip() for block in content_blocks]
        content = ' '.join(content_blocks)

        date = response.css('div.news-page__date::text').get()
        date = get_date_from_text(date)
        article = Article(title=title, content=content, date=date)
        yield article
