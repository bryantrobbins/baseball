#!/bin/bash -e

chmod 700 *.sh
./extract.sh
zip -r data.zip lahman/ gamelogs/

# Upload
aws s3 cp data.zip s3://baseball-workbench-builds/data/data-${CODEBUILD_BUILD_ID}.zip
