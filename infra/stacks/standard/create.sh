#!/bin/bash

# This script utilizes the awscli and its cloudformation functionality
# to deploy a stack defined by the 'cloud.json' template to the user's
# configured AWS environment within the us-east-1 region

# Accepts optional user inputs to define:
#  $1. Stack name
#  $2. Key Pair
#  $3. Region
# Note: To do: Add parsing and accept as variables

# Get options
tname="cloud.json"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"
sname=${1:-BTR-standard}
kname=${2:-builder}
rname=${3:-us-east-1}

# Determine if running on Windows (affects template file argument to aws cli)
platform=`uname`
if [[ ${platform} == *"MINGW"* ]]; then
  echo "Using Windows file path"
  tfile=`cygpath -w ${tfile} | sed -e 's/[\/]/\/\//g'`
else
  echo "Using Linux file path"
fi

# If user did not specify a key pair, create and save a new one to be used
if [ -z "$2" ]
  then
    echo "Creating new EC2 key pair and saving locally to builder.pem"
    # Delete any old keypair with same name
    aws ec2 delete-key-pair --key-name ${kname} --region us-east-1
    # Create and save EC2 key pair
    aws ec2 create-key-pair --key-name ${kname} --output text --region us-east-1 | sed 's/.*BEGIN.*-$/-----BEGIN RSA PRIVATE KEY-----/' | sed "s/.*${kname}$/-----END RSA PRIVATE KEY-----/" > ${kname}.pem
    chmod 600 ${kname}.pem
  else
    echo "Using user specified key pair: $kname"
fi

# Build cmd
cmd="aws cloudformation create-stack --stack-name $sname --template-body \"file://${tfile}\" --capabilities CAPABILITY_IAM --region $rname --parameters ParameterKey=KeyName,ParameterValue=${kname}"

# Tell user what is being done and execute cmd
echo "Creating stack '$sname' with keypair '$kname' in '$rname' region"
eval $cmd
