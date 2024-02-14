import asyncio

import pytest as pytest

from services.rabbitmq.broker import RabbitMQProducer
from tests.conftest import queue_name, dead_queue_name


@pytest.mark.asyncio
async def test_send_message(rabbitmq_connection, initialize_ent):
    rabbitmq_connection.settings.message_ttl = 100

    text_message = 'Test text message'
    producer = RabbitMQProducer(rabbitmq_connection)
    await producer.send_message(text_message)

    queue = await rabbitmq_connection.channel.get_queue(queue_name)
    message = await queue.get(fail=False, no_ack=True)
    assert message.body.decode() == text_message


@pytest.mark.asyncio
async def test_send_message_and_wait(rabbitmq_connection, initialize_ent):
    rabbitmq_connection.settings.message_ttl = 1

    text_message = 'Test text message'
    producer = RabbitMQProducer(rabbitmq_connection)
    await producer.send_message(text_message)

    await asyncio.sleep(1)

    queue = await rabbitmq_connection.channel.get_queue(queue_name)
    message = await queue.get(fail=False, no_ack=True)

    assert message is None

    dead_queue = await rabbitmq_connection.channel.get_queue(dead_queue_name)
    dead_message = await dead_queue.get(fail=False, no_ack=True)
    assert dead_message.body.decode() == text_message
