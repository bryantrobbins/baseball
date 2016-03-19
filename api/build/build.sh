#!/bin/bash -v

# Add js build steps here (npm, etc.)
npm install
npm run build

# Fetch AWS ECR variables
version=$1
chmod 700 fetch.sh
./fetch.sh $version > variables.json

# Build docker image with packer
packer="/usr/local/bin/packer"
$packer build -var-file=variables.json backend.json
