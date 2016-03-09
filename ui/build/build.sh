#!/bin/bash -v

# Add js build steps here (npm, etc.)
npm install
npm run build

# Fetch AWS ECR variables
chmod 700 fetch.sh
./fetch.sh > variables.json

# Build docker image with packer
packer="/usr/local/bin/packer"
$packer build frontend.json
