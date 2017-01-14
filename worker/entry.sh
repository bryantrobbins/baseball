#!/bin/bash

pushd /workdir
echo "Hello world" >> output.csv
aws s3 cp output.csv s3://baseball-workbench-data/output.csv
