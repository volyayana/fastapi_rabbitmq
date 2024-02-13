import asyncio

from config.config import settings
from endpoints.messages import messages_router
from services.common import MyApp


app = MyApp(settings=settings)
app.include_router(messages_router)


@app.on_event("startup")
async def startup_event():
    await app.pika_producer_connection.connect()
    await app.pika_consumer_connection.connect()
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(app.pika_consumer.consume())


@app.on_event("shutdown")
async def startup_event():
    await app.pika_producer_connection.close()
    await app.pika_consumer_connection.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}
