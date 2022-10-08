import scrapy
from w3lib.html import remove_tags
from ..items import Article
from ..helpers import get_date_from_text

class RbSpider(scrapy.Spider):
    name = "rb"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10000
    }

    def start_requests(self):
        pages_amount = 5
        for page_id in range(4, pages_amount):
            url = f'https://rb.ru/tag/business/?page={page_id}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'https://rb.ru'
        print(response.css('a::text').getall())
        for link in response.css('a.news-item__read-more::attr(href)'):
            yield scrapy.Request(url=base_url + link.get(), callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.article-header__rubric-title::text').get()
        introduction = response.css('div.article__introduction p::text').get()
        content_blocks = response.css('div.article__content-block.abv > p::text').getall()
        content_blocks = [remove_tags(block).strip() for block in content_blocks]
        content = ' '.join([introduction] + content_blocks)

        date = response.css('time.article-header__date span::text').getall()[1]
        date = get_date_from_text(date)

        # article = Article(title=title, content=content, date=date)
        # yield article
