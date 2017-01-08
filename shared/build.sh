#!/bin/bash -e

# Install build tools
apt-get update
apt-get install -y zip

# Build package and dependencies
pip install -t packages .

# Build zip
cd packages
cp ../api.py .
zip -r btr3baseball.zip *
cd ..
