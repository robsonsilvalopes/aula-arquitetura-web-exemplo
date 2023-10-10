# Delete all containers using the following command:
#docker rm -f $(docker ps -a -q)
docker rm -f exemplo_sistema_controller_1 
docker rm -f exemplo_sistema_gateway_1 
docker rm -f exemplo_sistema_redis_1 
docker rm -f exemplo_sistema_webapp_1
docker rm -f exemplo_sistema_worker-planos_1
# Delete all containers using the following command:
#docker volume rm $(docker volume ls -q)
# docker image prune -a
docker image rm exemplo_sistema_controller
docker image rm exemplo_sistema_webapp
docker image rm exemplo_sistema_gateway
docker image rm exemplo_sistema_worker-planos
docker image rm exemplo_sistema_redis_1 
