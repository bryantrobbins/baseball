#!/bin/bash

packer="/usr/local/bin/packer"
$packer build analyze.json
docker import - baseball/analyze:latest < analyze.tar 
