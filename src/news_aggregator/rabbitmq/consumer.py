import pika
import json
import os
from ..infrastructure.logging import logger

def get_connection():
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    params = pika.URLParameters(url)
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        return None, None

def callback(ch, method, body):
    message = json.loads(body)
    logger.info(f"Received message: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_messages(queue):
    connection, channel = get_connection()
    if connection and channel:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue, on_message_callback=callback)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    else:
        print("Failed to consume messages: Connection to RabbitMQ not established.")