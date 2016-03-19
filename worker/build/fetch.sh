#!/bin/bash

# Get login details
login=`aws ecr --region us-east-1 get-login`

# Set variables
version=$1
set $login
repoPrefix=$9
repoPrefix=${repoPrefix:8}

# Write values to stdout
echo "{"
echo "  \"image_version\": \"$version\","
echo "  \"aws_ecs_password\": \"$6\","
echo "  \"aws_ecs_server\": \"$9\","
echo "  \"aws_ecs_repo\": \"$repoPrefix/baseball-worker\""
echo "}"
