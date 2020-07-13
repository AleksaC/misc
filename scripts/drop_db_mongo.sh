#!/usr/bin/env bash

set -eou pipefail

mongo --eval "db.dropDatabase();" $1
