import asyncio
import aio_pika
from async_retrying import retry
import redis
import json


QUEUE_NAME = "nums_to_sum_queue"


@retry(attempts=10)
async def main() -> None:

    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/",
    )
    print("Ready to receive!")

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 1 messages in advance
        await channel.set_qos(prefetch_count=1)

        # Declaring queue
        queue = await channel.declare_queue(QUEUE_NAME)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print("Received message")
                    message_dict = json.loads(message.body.decode())
                    num_sum: int = int(message_dict["first"]) + int(message_dict["second"])
                    r = redis.Redis(host='my_redis', port=6379, db=0)
                    r.set(message_dict["id"], num_sum)
                    r.expire(message_dict["id"], 600)
                    print("Added to redis")


if __name__ == "__main__":
    asyncio.run(main())
