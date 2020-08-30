#!/usr/bin/env/ bash

# This script squashes all commits into "legacy code" commit and force pushes it to master

set -eou pipefail

git push -f
