from fastapi import FastAPI

from services.rabbitmq.broker import RabbitMQConnection, RabbitMQProducer, RabbitMQConsumer, BrokerProducer, \
    BrokerConsumer


class MyApp(FastAPI):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer_connection = RabbitMQConnection(settings)
        self.consumer_connection = RabbitMQConnection(settings)

        self.producer: BrokerProducer = RabbitMQProducer(connection=self.producer_connection)
        self.consumer: BrokerConsumer = RabbitMQConsumer(connection=self.consumer_connection)
