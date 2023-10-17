# Delete all containers using the following command:
#docker rm -f $(docker ps -a -q)
docker rm -f aula_02_redis_1
docker rm -f aula_02_webapp_1
docker rm -f aula_02_controller_1
docker rm  -f aula_02_worker-planos_1
docker rm -f aula_02_gateway_1
# Delete all containers using the following command:
#docker volume rm $(docker volume ls -q)
# docker image prune -a
docker image rm aula_02_redis
docker image rm aula_02_webapp
docker image rm aula_02_controller
docker image rm aula_02_worker-planos
docker image rm aula_02_gateway
