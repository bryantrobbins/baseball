#!/bin/bash

# Install build tools
apt-get install -y zip

# Build package and dependencies
pip install -t .

# Build zip
cd packages
cp ../api.py .
zip -r btr3baseball.zip *
cd ..
