#!/bin/bash -e

chmod 700 *.sh
./extract.sh
zip -r data.zip lahman/ gamelogs/
