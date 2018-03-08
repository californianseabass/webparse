#!/bin/bash
docker ps -a | grep webparse | head -n 1 | awk '{ print $1}' | xargs docker start

