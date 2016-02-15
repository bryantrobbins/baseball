#!/bin/bash

pushd /workdir
echo $(base64 -d <<< $1) > config.yaml
Rscript generic.R
