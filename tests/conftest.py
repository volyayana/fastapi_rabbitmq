import os

import pytest_asyncio
from dotenv import load_dotenv

from services.rabbitmq.broker import RabbitMQConnection

load_dotenv("fixtures/test.environment", override=True)

from config.config import settings


dead_exchange = os.getenv('DEAD_EXCHANGE')
queue_name = os.getenv('QUEUE_NAME')
dead_queue_name = os.getenv('DEAD_QUEUE_NAME')

@pytest_asyncio.fixture
async def rabbitmq_connection():
    connection = RabbitMQConnection(settings)
    await connection.connect()
    yield connection
    await connection.close()


@pytest_asyncio.fixture
async def initialize_ent(rabbitmq_connection):
    await rabbitmq_connection.initialize_entities()
    yield None
    await rabbitmq_connection.channel.queue_delete(dead_queue_name)
    await rabbitmq_connection.channel.queue_delete(queue_name)
    await rabbitmq_connection.channel.exchange_delete(dead_exchange)


