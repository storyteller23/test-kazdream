import pika
import json
import sqlite3

db_connection = sqlite3.connect('db.sqlite')
cursor = db_connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS product(
                    articul INT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    price TEXT,
                    category TEXT,
                    description TEXT,
                    photo_urls TEXT )''')


rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbitmq_connection.channel()
channel.queue_declare(queue='item', durable=True)


def callback(ch, method, properties, body):
    data = json.loads(body)
    info = cursor.execute('SELECT * FROM product WHERE articul = ?', (data['articul'],))
    if not info.fetchone():
        cursor.execute('INSERT INTO product(articul, name, price, category, description, photo_urls) VALUES(?, ?, ?, ?, ?, ?)',
                       (data['articul'], data['name'], data['price'], data['category'], data['description'],
                        ', '.join(data['photo_urls'])))
        db_connection.commit()

channel.basic_consume(queue='item', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
