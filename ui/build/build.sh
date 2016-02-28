#!/bin/bash -v

# Add js build steps here (npm, etc.)
npm install
npm run build

# Build docker image with packer
packer="/usr/local/bin/packer"
$packer build frontend.json
