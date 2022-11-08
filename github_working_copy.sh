#!/bin/bash

# Based on https://gist.github.com/kekru/88808f7dfbdcc5375cfcc99f9812d19f#file-git-copy-files-to-empty-branch-md

TODAY=$(date +"%Y-%m-%d")
TARGET_BRANCH="working_$TODAY"
CURRENT_BRANCH="$(git branch --show-current)"

echo -e "\nCreating a copy of current branch ( $CURRENT_BRANCH ) to backup branch ( $TARGET_BRANCH )\n"

git branch -D $TARGET_BRANCH

# First be sure, that you don't have uncommitted working changes. They will be deleted
# Checkout a new empty branch without history
git checkout --orphan $TARGET_BRANCH

# clear index and working tree
git rm -rf .

# Create empty commit
echo "Working code copy done at $TODAY" > info.md && git add info.md && git commit -m "Working code copy done at $TODAY"

# Merge the old branch to new one, using a squash
git merge --squash $CURRENT_BRANCH --allow-unrelated-histories

# Perform a commit, because the squash merge did not create a commit yet
git commit -m "Working code copy done at $TODAY"

git checkout $CURRENT_BRANCH

# Display all branches containing copies
echo "========================================================"
echo -e "\nAll branches containing working copies:"
git branch | grep -i work
echo
