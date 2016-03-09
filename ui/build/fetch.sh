#!/bin/bash

login=`aws ecr --region us-east-1 get-login`
set $login
echo "{"
echo "  \"aws_ecs_password\": \"$6\""
echo "  \"aws_ecs_server\": \"$9\""
echo "}"
