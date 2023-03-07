from aiokafka import AIOKafkaConsumer
from async_retrying import retry
import asyncio


TOPIC_NAME = "summed_nums"


@retry(attempts=5)
async def consume() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers='kafka-server:9092')

    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())
