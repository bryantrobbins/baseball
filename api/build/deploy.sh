#!/bin/bash

cd packages
aws s3 cp api.zip s3://baseball-workbench-builds/api/api-${CODEBUILD_BUILD_ID}.zip
aws lambda update-function-code --function-name baseball-api --s3-bucket baseball-workbench-builds --s3-key api/api-${CODEBUILD_BUILD_ID}.zip
