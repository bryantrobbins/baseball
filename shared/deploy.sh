#!/bin/bash

cd packages
aws s3 cp btr3baseball.zip s3://baseball-workbench-builds/btr3baseball/btr3baseball-${CODEBUILD_BUILD_ID}.zip
aws lambda update-function-code --function-name baseball-submitJob --s3-bucket baseball-workbench-builds --s3-key btr3baseball/btr3baseball-${CODEBUILD_BUILD_ID}.zip
aws lambda update-function-code --function-name baseball-getJobInfo --s3-bucket baseball-workbench-builds --s3-key btr3baseball/btr3baseball-${CODEBUILD_BUILD_ID}.zip
