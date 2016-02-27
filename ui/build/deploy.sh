#!/bin/bash

# Import docker image with tag
docker stop ui00
docker rm ui00
docker rmi baseball/ui
docker import - baseball/ui:latest < frontend.tar
docker run -d --name ui00 -p 80:80 baseball/ui:latest /usr/sbin/nginx -g 'daemon off;'
