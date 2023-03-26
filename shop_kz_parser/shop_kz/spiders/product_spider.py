import scrapy
import re

from shop_kz.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'shopkz'

    start_urls = ['https://shop.kz/catalog/']

    category_urls = set()

    def parse(self, response):
        for cat_link in response.css('.bx_catalog_tile_title a::attr("href")').getall():
            yield response.follow(cat_link, callback=self.parse_page_or_categories)

    def parse_page_or_categories(self, response):
        if response.url in self.category_urls:
            return

        if response.css('.bx_catalog_tile_title a'):
            for cat_link in response.css('.bx_catalog_tile_title a::attr(href)').getall():
                yield response.follow(cat_link, callback=self.parse_page_or_categories)

        if response.css('.bx_catalog_item_title'):
            self.category_urls.add(response.url)

            for product_link in response.css('.bx_catalog_item_title a::attr(href)').getall():
                yield response.follow(product_link, callback=self.parse_product_data)

            next_page = response.css('.bx_blue+ .bx-blue .bx-pag-next a::attr(href)')

            if next_page:
                yield response.follow(next_page.get(), callback=self.parse_page_or_categories)

    def parse_product_data(self, response):
        item = ProductItem()
        item['name'] = response.css('#pagetitle::text').get().strip()
        item['articul'] = response.css('.bx-card-mark li:nth-child(1)::text').get().split()[1]

        price = response.css('.item_current_price::text').get()
        if price:
            item['price'] = price.strip().replace(' ₸', '').replace(' ', '')
        else:
            item['price'] = ''

        item['category'] = response.css('#bx_breadcrumb_1 span::text').get().strip()
        item['description'] = ''.join(response.css('.bx_item_description::text').getall()).replace('\r\n', '').strip()
        photo_urls = []
        for style_string in response.css('.cnt_item::attr(style)').getall():
            url = 'https:' + style_string.replace("background-image:url('", '').replace("');", '')
            url = url.replace('/100_100_1', '').replace('/resize_cache', '')
            photo_urls.append(url)

        item['photo_urls'] = photo_urls

        yield item
