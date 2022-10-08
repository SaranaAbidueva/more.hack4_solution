import scrapy
from w3lib.html import remove_tags
from ..items import Article
import re

class GazetaSpider(scrapy.Spider):
    name = "gazeta"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10000
    }

    def start_requests(self):
        url = 'https://www.gazeta.ru/business/news/'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'https://www.gazeta.ru'
        for link in response.css('div#_id_article_listing a.m_techlisting::attr(href)'):
            yield scrapy.Request(url=base_url + link.get(), callback=self.parse_article)
        next_page_link = response.css('a.b_showmorebtn-link::attr(href)').get()
        yield scrapy.Request(url=base_url + next_page_link, callback=self.parse)

    def parse_article(self, response):
        tag = response.css('a.topic-header__item::text').get()
        title = response.css('h1.headline::text').get()

        content_blocks = response.css('div.b_article-text p').getall()
        content_blocks = [remove_tags(block) for block in content_blocks]
        content = ' '.join(content_blocks)

        url = response.request.url
        pattern = r'(/\d*/\d+/\d+/)'
        date = re.search(pattern, url).group(1)
        date = f'{date[9:11]}.{date[6:8]}.{date[1:5]}'
        article = Article(title=title, content=content, date=date)
        yield article
