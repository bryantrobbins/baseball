#!/bin/bash

# Get options
tname="cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"

# Create stack
aws cloudformation create-stack --stack-name baseball --template-body file:///${tfile} --region us-east-1
