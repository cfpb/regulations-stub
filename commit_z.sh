#!/bin/sh

COMMIT_MESSAGE=$1
REG='1026'
FILES=`git status --porcelain | grep $REG | grep -v \? | sed 's/\s*[MADRCU]\s*//'`

# Commit them one at a time
while read -r file; do
    git commit --no-verify -m "$COMMIT_MESSAGE" $file
    echo "Committed $file"
done <<< "$FILES"
