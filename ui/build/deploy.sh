#!/bin/bash

# Import docker image with tag
docker import - baseball/ui:latest < frontend.tar
docker run --rm --name ui00 baseball/ui:latest
