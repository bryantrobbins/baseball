#!/bin/bash

# Get options
tname="cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"
kname="builder"

# Create stack
aws cloudformation update-stack --stack-name BTR-standard --template-body file:///${tfile} --parameters ParameterKey=KeyName,ParameterValue=${kname} --capabilities CAPABILITY_IAM
