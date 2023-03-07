docker network create my_network
docker run -d --network my_network --hostname rabbitmqhost \
   --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
docker run --name my_redis -p 6379:6379 -d --network my_network redis
docker build -t data_entry ./data-entry
docker build -t data_proccess ./data-proccess
docker build -t results_view ./results-view
docker run -d --name data_entry_cont --network my_network -p 80:80 data_entry
docker run -d --name data_proccess_cont --network my_network data_proccess
docker run -d --name results_view_cont --network my_network -p 81:80 results_view
#docker run --name data_proccess_cont --network my_network data_proccess

