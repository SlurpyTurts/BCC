# bcc-db

The database side of the BCC project

## How to get the database running

Make sure you have docker installed and running, then from this folder run

```
docker run --name bcc-db -e MYSQL_ROOT_PASSWORD=my-secret-pw \
-v $(pwd):/etc/bcc -p 3306:3306 -p 33060:33060 mysql/mysql-server:latest

docker exec -t bcc-db /bin/bash /etc/bcc/initialize_docker_mysql_db.sh
```

## Tearing down database

When you want to shut down and remove the database

```
docker stop bcc-db
docker rm bcc-db

```
