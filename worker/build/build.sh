#!/bin/bash -v

# Add R build steps here (if any)
#pushd extract
#./extract.sh
#popd
#Rscript Build.R
#mv baseball/staging

# Install packer
pversion="0.12.1"
purl="https://releases.hashicorp.com/packer/${pversion}/packer_${pversion}_linux_amd64.zip"
wget $purl
unzip packer_${pversion}_linux_amd64.zip

# Fetch AWS ECR variables
version=$1
chmod 700 fetch.sh
./fetch.sh $version > variables.json

# Build docker image with packer
packer="./packer"
$packer build -var-file=variables.json worker.json
