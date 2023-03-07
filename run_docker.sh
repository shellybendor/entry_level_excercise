docker network create my_network
docker run -d --network my_network --hostname rabbitmqhost \
   --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
docker run --name my_redis -p 6379:6379 -d --network my_network redis

# start apache kafka server
docker run -d --name zookeeper-server \
    --network my_network \
    -e ALLOW_ANONYMOUS_LOGIN=yes \
    bitnami/zookeeper:latest
docker run -d --name kafka-server \
    --network my_network \
    -e ALLOW_PLAINTEXT_LISTENER=yes \
    -e KAFKA_AUTO_CREATE_TOPICS_ENABLE=true \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181 \
    bitnami/kafka:latest

docker run -dp 10000:10000 --name azurite --network my_network mcr.microsoft.com/azure-storage/azurite
docker build -t kafka_reader ./kafka-reader
docker run -d --name kafka_reader_cont --network my_network kafka_reader
docker build -t data_entry ./data-entry
docker build -t data_proccess ./data-proccess
docker build -t results_view ./results-view
docker run -d --name data_entry_cont --network my_network -p 80:80 data_entry
docker run -d --name data_proccess_cont --network my_network data_proccess
docker run -d --name results_view_cont --network my_network -p 81:80 results_view
