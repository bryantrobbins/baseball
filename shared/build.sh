#!/bin/bash

# Build package and dependencies
pip install -t .

# Build zip
cd packages
cp ../api.py .
zip -r btr3baseball.zip *
cd ..
