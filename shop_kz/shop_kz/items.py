# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    articul = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    photo_urls = scrapy.Field(output_processor=True)
