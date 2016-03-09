#!/bin/bash

# Get login details
login=`aws ecr --region us-east-1 get-login`

# Set variables
set $login
repoPrefix=$9
repoPrefix=${repoPrefix:8}

# Write values to stdout
echo "{"
echo "  \"aws_ecs_password\": \"$6\","
echo "  \"aws_ecs_server\": \"$9\","
echo "  \"aws_ecs_repo\": \"$repoPrefix/baseball-ui\""
echo "}"
