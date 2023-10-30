# Delete all containers using the following command:
#docker rm -f $(docker ps -a -q)
docker rm -f aula_03_redis_1
docker rm -f aula_03_webapp_1
docker rm -f aula_03_controller_1
docker rm  -f aula_03_worker-math_1
docker rm -f aula_03_gateway_1
# Delete all containers using the following command:
#docker volume rm $(docker volume ls -q)
# docker image prune -a
docker image rm aula_03_redis
docker image rm aula_03_webapp
docker image rm aula_03_controller
docker image rm aula_03_worker-math
docker image rm aula_03_gateway
