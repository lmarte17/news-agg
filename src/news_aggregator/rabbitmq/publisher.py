import pika
import json
import os
from ..infrastructure.models.article import ArticleModel as Article

def get_connection():
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    params = pika.URLParameters(url)
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        print("Successfully connected to RabbitMQ")
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        return None, None

def publish_message(queue, message):
    connection, channel = get_connection()
    if connection and channel:
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
        print(f"Published message to {queue}")
        connection.close()
    else:
        print("Failed to establish a connection with RabbitMQ.")