from src.news_aggregator.rabbitmq.consumer import consume_messages

if __name__ == '__main__':
    consume_messages('article_queue')