#!/bin/sh
# Scheduled entry point for the FLOWIE sweep: runs flowie-sweep.sh and posts a
# macOS notification when it exits nonzero (invariant failures, or the run
# itself errored). The launchd agent in operator/net.zunigo.flowie-sweep.plist
# calls this; the sweep's own exit code is passed through unchanged.
#
# The notification text is only ever the sweep script's own last status line,
# never model output, and is handed to osascript as an argument, not as code.

set -u
cd "$(dirname "$0")/.."

code=0
out=$(sh scripts/flowie-sweep.sh 2>&1) || code=$?
printf '%s  exit=%s\n%s\n' "$(date '+%Y-%m-%d %H:%M')" "$code" "$out"

if [ "$code" -ne 0 ]; then
  msg=$(printf '%s\n' "$out" | tail -n 1)
  osascript \
    -e 'on run argv' \
    -e 'display notification (item 1 of argv) with title "FLOWIE sweep" subtitle (item 2 of argv)' \
    -e 'end run' \
    "$msg" "See operator/reports/ in the FLOWIE repo" || true
fi

exit "$code"
