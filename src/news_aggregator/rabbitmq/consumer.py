import pika
import json

def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    return connection, channel

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")
    # Process the message (e.g., perform NLP tasks, store in database)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_messages(queue):
    connection, channel = get_connection()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()