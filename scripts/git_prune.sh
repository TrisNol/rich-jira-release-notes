#!/bin/bash

# Fetch all branches and prune deleted branches from the remote
git fetch --prune

# Get a list of all local branches that have been deleted from the remote
deleted_branches=$(git branch -vv | grep ': gone]' | awk '{print $1}')

# Loop through the list and delete each branch locally
for branch in $deleted_branches; do
    git branch -D $branch
done
