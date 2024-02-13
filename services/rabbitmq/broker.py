from abc import ABC, abstractmethod

import aio_pika
from aio_pika import Message, DeliveryMode
from aio_pika.abc import AbstractIncomingMessage


class BrokerConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass


class BrokerProducer(ABC):
    @abstractmethod
    def send_message(self):
        pass


class BrokerConsumer(ABC):
    @abstractmethod
    def consume(self):
        pass


class RabbitMQConnection(BrokerConnection):
    def __init__(self, settings):
        self.settings = settings
        self.connection = None
        self.channel = None
        self.queue = None
        self.dead_queue = None
        self.dead_exchange = None

    async def initialize_entities(self):
        self.dead_exchange = await self.channel.declare_exchange(
            self.settings.dead_exchange,
            aio_pika.ExchangeType.FANOUT,
        )
        self.dead_queue = await self.channel.declare_queue(
            self.settings.dead_queue_name,
            durable=True,
        )
        await self.dead_queue.bind(self.dead_exchange, self.settings.dead_routing_key)

        self.queue = await self.channel.declare_queue(
            self.settings.queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self.settings.dead_exchange,
                "x-dead-letter-routing-key": self.settings.dead_routing_key,
            }
        )

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            url=self.settings.amqp_dsn,
        )
        self.channel = await self.connection.channel()
        await self.initialize_entities()

    async def close(self):
        await self.connection.close()


class RabbitMQProducer(BrokerProducer):
    def __init__(self, connection):
        self.connection = connection

    async def send_message(self, message_text):
        message = Message(
            body=message_text.encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            expiration=self.connection.settings.message_ttl,
        )
        await self.connection.channel.default_exchange.publish(
            message=message,
            routing_key=self.connection.settings.queue_name,
        )


class RabbitMQConsumer(BrokerConsumer):
    def __init__(self, connection):
        self.connection = connection

    async def consume(self):
        await self.connection.channel.set_qos(10)
        await self.connection.queue.consume(self.process_message, no_ack=False)

    @staticmethod
    async def process_message(
        message: AbstractIncomingMessage,
    ):
        await message.ack()
        print('We got a message: %s' % message.body)
