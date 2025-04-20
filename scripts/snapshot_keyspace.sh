#!/usr/bin/env bash
set -euo pipefail
# Take and prune snapshots for keyspace $KS (default gibsey)
KS="${1:-gibsey}"
STAMP=$(date +%Y%m%d-%H%M%S)
echo "▶︎ snapshot $KS  $STAMP"
nodetool snapshot "$KS" -t "$STAMP"
# prune older than 7 days
find /var/lib/cassandra/data/$KS -type d -name 'snapshots' -exec find {} -maxdepth 1 -mtime +7 -type d -exec rm -rf {} + \
    ;