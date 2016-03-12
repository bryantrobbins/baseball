#!/bin/bash

./clean.sh

echo "Download groovy (temp)"
wget -O groovy.jar http://search.maven.org/remotecontent?filepath=org/codehaus/groovy/groovy/2.4.6/groovy-all-2.4.6.jar

echo "Download and transform raw data"
pushd extract
java -jar ../groovy.jar download.groovy
popd

echo "Create redistributable package"
Rscript Build.R
