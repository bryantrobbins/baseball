#!/bin/bash -v

# Data bundle version
version="data-data%3A55a8fba4-c190-4e77-a379-a09f53e372ec.zip"

# Install packer
pversion="0.12.1"
purl="https://releases.hashicorp.com/packer/${pversion}/packer_${pversion}_linux_amd64.zip"
wget $purl
unzip packer_${pversion}_linux_amd64.zip

# Create staging dir
mkdir staging

# Pull extracted data
cd staging
aws s3 cp s3://${version}
unzip ${version}
rm ${version}
cd ..

# Fetch AWS ECR variables
version=${IMAGE_VERSION}
chmod 700 fetch.sh
./fetch.sh $version > variables.json

# Build docker image with packer
packer="./packer"
$packer build -var-file=variables.json worker.json
