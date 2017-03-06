#!/bin/bash -e

# Data bundle version
version="data-data:55a8fba4-c190-4e77-a379-a09f53e372ec.zip"

# Build python code
cd ../../shared
rm -rf packages
pip install . -t packages
cd ../worker/build

# Create staging dir
rm -rf staging
mkdir staging

# Pull extracted data
cd staging
aws s3 cp s3://baseball-workbench-builds/data/${version} .
unzip ${version}
rm ${version}
cd ..

# Copy over additional scripts
cp -r ../../shared/packages/* staging
cp prepare.R staging
cp ../app.py staging

# Fetch AWS ECR variables
version=${IMAGE_VERSION}
chmod 700 fetch.sh
./fetch.sh $version > variables.json

# Build docker image with packer
packer="packer"
$packer build -var-file=variables.json worker.json
