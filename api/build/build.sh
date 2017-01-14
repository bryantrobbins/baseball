#!/bin/bash -e

# Install build tools
apt-get update
apt-get install -y zip

# Build package and dependencies
cd ../shared
pip install -t packages .
cd ../api

# Build zip
mv ../shared/packages .
cd packages
cp ../api.py .
zip -r api.zip *
cd ..
