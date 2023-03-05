docker network create my_network
docker build -t data_entry ./data_entry
docker run -d --name data_entry_cont --network my_network -p 80:80 data_entry
docker run -d --network my_network --hostname rabbitmqhost \
   --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management

