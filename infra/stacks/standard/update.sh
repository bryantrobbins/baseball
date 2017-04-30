#!/bin/bash

# This script utilizes the awscli and its cloudformation functionality
# to update the stack within the user's configured AWS environment
# with the current template definition within the 'cloud.json'

# Accepts optional user inputs to define:
#  $1. Stack name
#  $2. Key Pair
# Note: To do: Add parsing and accept as variables

# Get options
tname="cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"
sname=${1:-BTR-standard}
kname=${2:-builder}

# Determine if running on Windows (affects template file argument to aws cli)
platform=`uname`
if [[ ${platform} == *"MINGW"* ]]; then
  echo "Using Windows file path"
  tfile=`cygpath -w ${tfile} | sed -e 's/[\/]/\/\//g'`
else
  echo "Using Linux file path"
fi

# Update stack
cmd="aws cloudformation update-stack --stack-name $sname --template-body "file://${tfile}" --parameters ParameterKey=KeyName,ParameterValue=${kname} --capabilities CAPABILITY_IAM"

# Tell user what is being done and execute cmd
echo "Updating stack '$sname' with keypair '$kname'"
echo $cmd