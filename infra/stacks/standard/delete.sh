#!/bin/bash

# This script utilizes the awscli and its cloudformation functionality
# to delete the referenced stack within the user's configured AWS environment

# Accepts optional user input to define:
#  $1. Stack name

# Get options
tname="../cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"
sname=${1:-BTR-standard}

# Delete stack
cmd="aws cloudformation delete-stack --stack-name $sname"

# Tell user what is being done and execute cmd
echo "Deleting stack '$sname'"
eval $cmd
