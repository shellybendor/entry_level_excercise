import msgpack
import aio_pika
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from typing import Union
from uuid import UUID, uuid4


class TwoInts(BaseModel):
    first: int
    second: int
    id: Union[UUID, None] = None


app = FastAPI()


async def pub_to_queue(two_ints: TwoInts) -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")

    async with connection:
        routing_key = "nums_to_sum_queue"  # TODO: make global?

        channel = await connection.channel()
        queue = await channel.declare_queue(routing_key)

        await channel.default_exchange.publish(
            aio_pika.Message(body=msgpack.packb(two_ints)),
            routing_key=queue.name,
        )


@app.post("/sum")
async def send_nums(two_ints: TwoInts, background_tasks: BackgroundTasks):
    if not two_ints.id:
        two_ints.id = uuid4()
    background_tasks.add_task(pub_to_queue, two_ints)
    return {"id": str(two_ints.first) + str(two_ints.second)}
    # return two_ints
