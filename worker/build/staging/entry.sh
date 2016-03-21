#!/bin/bash

outfile=$1
pushd /workdir
echo $(base64 -d <<< $2) > config.json
#Rscript generic.R
# For testing, just copy input as output
# This output should really be created by the R script
mv config.json output.csv
aws s3 cp output.csv --acl public-read s3://baseball-workbench/$1

