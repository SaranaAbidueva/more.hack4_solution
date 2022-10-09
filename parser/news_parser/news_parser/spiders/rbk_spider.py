import scrapy
from w3lib.html import remove_tags
from ..items import Article
from ..helpers import get_date_from_url


class RBKSpider(scrapy.Spider):
    name = "rbk"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10000
    }

    def start_requests(self):
        pages_amount = 100
        limit = 15

        for page_id in range(pages_amount):
            url = f'https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=business&offset={limit * page_id}&limit={limit}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.css('a::attr(href)'):
            yield scrapy.Request(url=link.get()[2:-2], callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.article__header__title-in::text').get()
        # print(title)
        content_blocks = response.css('div.article__text p::text').getall()
        content_blocks = [remove_tags(block).strip().replace('\xa0', ' ') for block in content_blocks]
        content = ' '.join(content_blocks)

        url = response.request.url
        date = get_date_from_url(url, 'rus')
        article = Article(title=title, content=content, date=date, url=url)
        yield article
