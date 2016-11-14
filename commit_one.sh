#!/bin/sh

REG=$1
COMMIT_MESSAGE=$2
FILES=`git status --porcelain | grep $REG | grep -v \? | sed 's/\s*[MADRCU]\s*//'`

# Commit them one at a time
while read -r file; do
    git commit --no-verify -m "$COMMIT_MESSAGE" $file
    echo "Committed $file"
done <<< "$FILES"
