import pika
import json
import sqlite3

from config import DB_NAME, RABBITMQ_HOST, RABBITMQ_QUEUE

db_connection = sqlite3.connect(DB_NAME)
cursor = db_connection.cursor()
print(RABBITMQ_HOST)
print('*' * 10)
cursor.execute('''CREATE TABLE IF NOT EXISTS product(
                    articul INT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    price TEXT,
                    category TEXT,
                    description TEXT,
                    photo_urls TEXT )''')

rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = rabbitmq_connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)


def callback(ch, method, properties, body):
    data = json.loads(body)
    info = cursor.execute('SELECT * FROM product WHERE articul = ?', (data['articul'],))
    if not info.fetchone():
        cursor.execute(
            'INSERT INTO product(articul, name, price, category, description, photo_urls) VALUES(?, ?, ?, ?, ?, ?)',
            (data['articul'], data['name'], data['price'], data['category'], data['description'],
             ', '.join(data['photo_urls'])))
        db_connection.commit()


channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

if __name__ == '__main__':
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
