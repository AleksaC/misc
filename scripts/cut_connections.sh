#!/usr/bin/env bash

set -eou pipefail

echo "Terminating all connections to $1"

sudo -u postgres psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid) \
                          FROM pg_stat_activity \
                          WHERE pg_stat_activity.datname = '$1'"
