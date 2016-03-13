#!/bin/bash

# Get options
stack=$1

# Delete stack
aws cloudformation delete-stack --stack-name baseball-$stack
