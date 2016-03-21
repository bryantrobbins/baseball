#!/bin/bash -v

# Add R build steps here (if any)

pushd extract
./extract.sh
popd
#Rscript Build.R

# Fetch AWS ECR variables
#version=$1
#chmod 700 fetch.sh
#./fetch.sh $version > variables.json

# Build docker image with packer
#packer="/usr/local/bin/packer"
#$packer build -var-file=variables.json worker.json
