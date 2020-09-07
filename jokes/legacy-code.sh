#!/usr/bin/env bash

# This script squashes all commits into "legacy code" commit and force pushes it to master

set -eou pipefail

git reset $(git rev-list HEAD | tail -n 1)
git add .
git commit --amend -m "Legacy code"
git push -f
