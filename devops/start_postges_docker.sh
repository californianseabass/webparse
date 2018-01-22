#!/bin/bash
#docker run -p 5432:5432 amoebas/postgres:v0.0.1 postgres
docker ps -a | tail -n +2 | awk '{ print $1 }' | xargs docker rm
packer build postgres.json
docker-compose up

