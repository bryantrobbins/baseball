#!/bin/bash

outfile=$1
pushd /workdir
echo $(base64 -d <<< $2) > config.json
Rscript getData2.R
aws s3 cp output.csv --acl public-read s3://baseball-workbench/$1
