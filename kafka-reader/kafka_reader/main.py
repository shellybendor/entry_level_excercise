from aiokafka import AIOKafkaConsumer
from async_retrying import retry
from azure.storage.blob.aio import BlobClient, ContainerClient
import asyncio


CONN_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;" \
              "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuF" \
              "q2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://" \
              "azurite:10000/devstoreaccount1;QueueEndpoint=" \
              "http://azurite:10001/devstoreaccount1;TableEndpoint=http://" \
              "azurite:10002/devstoreaccount1;"
CONTAINER_NAME = "test-container"
TOPIC_NAME = "summed_nums"


async def get_blob_client() -> BlobClient:
    print("getting container")
    async with ContainerClient.\
            from_connection_string(conn_str=CONN_STRING,
                                   container_name=CONTAINER_NAME)\
            as container:
        await container.create_container()
    print("got container, getting blob client")
    blob = BlobClient.from_connection_string(conn_str=CONN_STRING,
                                             container_name=CONTAINER_NAME,
                                             blob_name="my_blob")
    return blob


@retry(attempts=2)
async def start_consumer() -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers='kafka-server:9092')
    print("starting consumer")
    await consumer.start()
    print("consumer started")
    return consumer


async def consume() -> None:
    blob, consumer = await asyncio.gather(get_blob_client(), start_consumer())
    message_log = []
    async with blob as blob_client:
        try:
            # Consume messages
            async for msg in consumer:
                message_log.append(msg.value)
                if len(message_log) == 5:
                    for m in message_log:
                        await blob_client.upload_blob(m,
                                                      blob_type="AppendBlob")
                    # # uncomment for debugging:
                    # blobstr = await blob_client.download_blob()
                    # blobstr = await blobstr.readall()
                    # print(blobstr.decode("utf-8"))
                    message_log = []

        finally:
            # Will leave consumer group; perform autocommit if enabled.
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
