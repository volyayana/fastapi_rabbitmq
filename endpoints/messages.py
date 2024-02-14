from fastapi import APIRouter, Request

from models.messages import Message

messages_router = APIRouter()


@messages_router.post("/message/")
async def send_message(
    message: Message,
    request: Request,
):
    await request.app.producer.send_message(message.message)
