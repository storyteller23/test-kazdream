import os

try:
    DB_NAME = os.environ['DB_NAME']
except KeyError:
    DB_NAME = 'db.sqlite'

try:
    RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
except KeyError:
    RABBITMQ_HOST = 'localhost'

try:
    RABBITMQ_QUEUE = os.environ['RABBITMQ_QUEUE']
except KeyError:
    RABBITMQ_QUEUE = 'item'
