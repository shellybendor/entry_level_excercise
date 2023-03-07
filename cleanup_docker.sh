docker rm -f data_entry_cont && docker rm -f data_proccess_cont && docker rm -f rabbitmq && docker rm -f my_redis
docker rm -f results_view_cont
docker network rm my_network