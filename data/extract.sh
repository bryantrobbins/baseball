#!/bin/bash

echo "Cleaning old files"
rm -rf lahman gamelogs tmp_*

echo "Download groovy (temp)"
wget -O groovy.jar http://search.maven.org/remotecontent?filepath=org/codehaus/groovy/groovy/2.4.6/groovy-all-2.4.6.jar

echo "Download and transform raw data"
java -jar groovy.jar download.groovy
