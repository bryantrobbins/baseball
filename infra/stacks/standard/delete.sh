#!/bin/bash

# Get options
tname="../cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"
kname="builder"

# Delete stack
aws cloudformation delete-stack --stack-name BTR-standard
