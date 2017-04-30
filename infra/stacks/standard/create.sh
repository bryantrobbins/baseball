#!/bin/bash

# This script utilizes the awscli and its cloudformation functionality
# to deploy a stack defined by the 'cloud.json' template to the user's
# configured AWS environment within the us-east-1 region

# Accepts optional user input ($1) to define the stack name
# Note: To do: Add other user input variables with better parsing
#  e.g. region, key-pair

# Get options
tname="cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"
sname=${1:-BTR-standard}

# Determine if running on Windows (affects template file argument to aws cli)
platform=`uname`
if [[ ${platform} == *"MINGW"* ]]; then
  echo "Using Windows file path"
  tfile=`cygpath -w ${tfile} | sed -e 's/[\/]/\/\//g'`
else
  echo "Using Linux file path"
fi

kname="builder"

# Delete old keypair
# To do: Would be nice to allow user to re-use an existing key-pair, and this block of functionality could be made optional
aws ec2 delete-key-pair --key-name ${kname} --region us-east-1

# Create and save EC2 key pair
aws ec2 create-key-pair --key-name ${kname} --output text --region us-east-1 | sed 's/.*BEGIN.*-$/-----BEGIN RSA PRIVATE KEY-----/' | sed "s/.*${kname}$/-----END RSA PRIVATE KEY-----/" > ${kname}.pem
chmod 600 ${kname}.pem

cmd="aws cloudformation create-stack --stack-name $sname --template-body \"file://${tfile}\" --capabilities CAPABILITY_IAM --region us-east-1 --parameters ParameterKey=KeyName,ParameterValue=${kname}"

# Execute cmd
echo $cmd
