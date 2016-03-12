#!/bin/bash

echo "Cleanup"
rm -rf baseball_*.tar.gz

pushd extract
rm -rf lahman gamelogs tmp_*
popd

pushd baseball
rm -rf data
popd
