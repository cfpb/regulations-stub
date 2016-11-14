#!/bin/sh

REG=$1
COMMIT_MESSAGE=$2
FILES=`git status --porcelain | grep $REG | grep -v \? | sed 's/\s*[MADRCU]\s*//'`

git commit --no-verify -m "$COMMIT_MESSAGE" $FILES
