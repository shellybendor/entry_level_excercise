from typing import Union
from uuid import UUID, uuid4

import aio_pika
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel


class TwoInts(BaseModel):
    first: int
    second: int
    id: Union[UUID, None] = None


app = FastAPI()
QUEUE_NAME = "nums_to_sum_queue"


async def pub_to_queue(two_ints: TwoInts) -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME)

        await channel.default_exchange.publish(
            aio_pika.Message(body=two_ints.json().encode()),
            routing_key=queue.name,
        )


@app.post("/sum")
async def send_nums(two_ints: TwoInts, background_tasks: BackgroundTasks):
    two_ints.id = uuid4()
    background_tasks.add_task(pub_to_queue, two_ints)
    return {"id": two_ints.id}
