#!/bin/bash

# Take in credentials.csv as argument
cfile=$1

if [ -z ${cfile} ]; then
  echo "You must provide a credentials file as the first arg to this script"
  exit -1
fi

# Get and parse credentials line
in=`sed '2q;d' ${cfile}`
IFS=',' read -ra ADDR <<< "${in}"

# Write credentials file
user=${ADDR[0]}
akey=${ADDR[1]}
skey=${ADDR[2]}
printf "[default]\naws_access_key_id=${akey}\naws_secret_access_key=${skey}\n" > ~/.aws/credentials

# Write config file with default options for the account
printf "[default]\nregion=us-east-1\noutput=json\n" > ~/.aws/config

echo "Done"
