#!/bin/bash

pushd /workdir
#Rscript generic.R
# This output should really be created by the R script
echo "Hello world" >> output.csv
aws s3 cp output.csv s3://baseball-workbench-data/output.csv
