#!/usr/bin/env sh

DIR=$(cd $(dirname "$0"); pwd)
cd $DIR

./bin/tinge &
./bin/blend 
