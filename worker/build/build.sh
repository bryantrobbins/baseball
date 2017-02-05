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

# Extract and stage data
cd ../extract
chmod 700 extract.sh
./extract.sh
mkdir ../build/staging
mv lahman ../build/staging
mv gamelogs ../build/staging
cd ../build

# Fetch AWS ECR variables
version=${IMAGE_VERSION}
chmod 700 fetch.sh
./fetch.sh $version > variables.json

# Build docker image with packer
packer="./packer"
$packer build -var-file=variables.json worker.json
