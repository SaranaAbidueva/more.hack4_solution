import scrapy
from w3lib.html import remove_tags
from ..items import Article

class LentaSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        url = 'https://lenta.ru/rubrics/economics/markets/'

        for page_id in range(50):
            yield scrapy.Request(url=url + page_id, callback=self.parse)

    def parse(self, response):
        base_url = 'https://lenta.ru/'
        for link in response.css('a.card-full-news::attr(href)'):
            yield scrapy.Request(url=base_url + link.get(), callback=self.parse_article)

    def parse_article(self, response):
        tag = response.css('a.topic-header__item::text').get()
        title = response.css('span.topic-body__title::text').get()

        content_blocks = response.css('p.topic-body__content-text').getall()
        content_blocks = [remove_tags(block) for block in content_blocks]
        content = ' '.join(content_blocks)

        url = response.request.url
        date = f'{url[31:33]}.{url[28:30]}.{url[23:27]}'

        article = Article(title=title, tag=tag, content=content, date=date)
        yield article

