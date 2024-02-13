from fastapi import FastAPI

from services.rabbitmq.broker import RabbitMQConnection, RabbitMQProducer, RabbitMQConsumer


class MyApp(FastAPI):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_producer_connection = RabbitMQConnection(settings)
        self.pika_consumer_connection = RabbitMQConnection(settings)
        self.pika_producer = RabbitMQProducer(connection=self.pika_producer_connection)
        self.pika_consumer = RabbitMQConsumer(connection=self.pika_consumer_connection)
