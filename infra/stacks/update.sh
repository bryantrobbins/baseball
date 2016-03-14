#!/bin/bash

# Get options
stack=$1
tname="${stack}.json"
pname="${stack}.properties"
tfile="$(cd "$(dirname "${tname}")"; pwd)/$(basename "${tname}")"

# Get ECSCluster parameter
cluster=`aws cloudformation describe-stack-resources --stack-name BTR-standard --region us-east-1 | jq -r '.StackResources[] | select(.LogicalResourceId == "ECSCluster") | .PhysicalResourceId'`

# See if stack already exists (determing update vs. create)
aws cloudformation describe-stacks --stack-name baseball-$stack > dscontent

if [[ -s dscontent ]]; then
  cmd="aws cloudformation update-stack --stack-name baseball-$stack --template-body file:///${tfile} --region us-east-1"
else
  cmd="aws cloudformation create-stack --stack-name baseball-$stack --template-body file:///${tfile} --region us-east-1"
fi


# Build parameters list
pargs=""
if [[ -a $pname ]]; then
  while read p; do
    key=`echo $p | tr "=" " " | awk '{print $1}'`
    if [[ "$key" == "ECSCluster" ]]; then
      value=$cluster
    else
      value=`echo $p | tr "=" " " | awk '{print $2}'`
    fi
    pargs="${pargs} ParameterKey=${key},ParameterValue=${value}"
    echo "Adding parameter ${key} with value ${value}"
  done <$pname
fi

if [[ -n $pargs ]]; then
  cmd="${cmd} --parameters ${pargs}"
fi

# Create stack
#echo $cmd
eval $cmd
