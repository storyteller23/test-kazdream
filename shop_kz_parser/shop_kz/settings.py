import os

BOT_NAME = "shop_kz"

SPIDER_MODULES = ["shop_kz.spiders"]
NEWSPIDER_MODULE = "shop_kz.spiders"

ROBOTSTXT_OBEY = True

try:
    RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
except KeyError:
    RABBITMQ_HOST = 'localhost'

try:
    RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
except KeyError:
    RABBITMQ_PORT = 5672

try:
    RABBITMQ_USER = os.environ['RABBITMQ_USER']
except KeyError:
    RABBITMQ_USER = 'guest'

try:
    RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
except KeyError:
    RABBITMQ_PASSWORD = 'guest'

try:
    RABBITMQ_VIRTUAL_HOST = os.environ['RABBITMQ_VIRTUAL_HOST']
except KeyError:
    RABBITMQ_VIRTUAL_HOST = "/"

try:
    RABBITMQ_EXCHANGE = os.environ['RABBITMQ_EXCHANGE']
except KeyError:
    RABBITMQ_EXCHANGE = "scrapy"

try:
    RABBITMQ_ROUTING_KEY = os.environ['RABBITMQ_ROUTING_KEY']
except KeyError:
    RABBITMQ_ROUTING_KEY = "item"

try:
    RABBITMQ_QUEUE = os.environ['RABBITMQ_QUEUE']
except KeyError:
    RABBITMQ_QUEUE = "item"

ITEM_PIPELINES = {
    "scrapy_rabbitmq_publisher.pipelines.RabbitMQItemPublisherPipeline": 1,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
