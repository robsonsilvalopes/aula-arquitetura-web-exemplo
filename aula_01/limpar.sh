# Delete all containers using the following command:
#docker rm -f $(docker ps -a -q)
docker rm -f aula_01_controller_1 
docker rm -f aula_01_gateway_1 
# Delete all containers using the following command:
#docker volume rm $(docker volume ls -q)
# docker image prune -a
docker image rm aula_01_controller
docker image rm aula_01_gateway

