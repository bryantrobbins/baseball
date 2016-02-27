#!/bin/bash

packer build analyze.json
docker import - baseball/analyze:latest < analyze.tar 
