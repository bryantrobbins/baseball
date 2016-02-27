#!/bin/bash

# Import docker image with tag
docker stop ui00
docker rmi bryantrobbins/ui
docker rm ui00
docker import - bryantrobbins/ui < frontend.tar
docker run -d --name ui00 -p 80:80 baseball/ui:latest /usr/sbin/nginx -g 'daemon off;'
