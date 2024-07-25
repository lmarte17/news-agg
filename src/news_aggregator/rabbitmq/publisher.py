import pika
import json
import os
from ..infrastructure.models.article import Article

def get_connection():
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return connection, channel

def publish_message(queue, message):
    connection, channel = get_connection()
    channel.queue_declare(queue=queue, durable=True)
    if isinstance(message, Article):
        message = message.to_dict()
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()