#!/bin/bash

# Get options
tname="../cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"

# Delete stack
aws cloudformation delete-stack --stack-name baseball
