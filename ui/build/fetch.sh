#!/bin/bash

login=`aws ecr get-login`
set $login
echo "{"
echo "  \"aws_ecs_password\": \"$6\""
echo "  \"aws_ecs_server\": \"$9\""
echo "}"
