import pytest as pytest
from aiormq import ChannelNotFoundEntity

from tests.conftest import dead_exchange, queue_name, dead_queue_name


@pytest.mark.asyncio
async def test_initialize_entities(rabbitmq_connection, initialize_ent):
    assert dead_exchange == (await rabbitmq_connection.channel.get_exchange(dead_exchange)).name
    assert queue_name == (await rabbitmq_connection.channel.get_queue(queue_name)).name
    assert dead_queue_name == (await rabbitmq_connection.channel.get_queue(dead_queue_name)).name


@pytest.mark.asyncio
async def test_not_initialize_entities(rabbitmq_connection):
    with pytest.raises(ChannelNotFoundEntity):
        await rabbitmq_connection.channel.get_exchange(dead_exchange)
