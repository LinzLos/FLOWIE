#!/bin/sh
# FLOWIE .xml/.txt parity guard.
#
# The script ships as two hand-maintained files that must stay identical,
# except that the .txt opens with a short usage preamble before its "<?xml"
# line. This check fails if they differ anywhere else. (The v2.6 .xml silently
# lost the <heuristics_reference> block this way — see issue #4.)
#
# Usage, from the repo root:
#   scripts/check_parity.sh                # checks the pair in manifest.json
#   scripts/check_parity.sh FILE.xml FILE.txt   # checks an explicit pair
#
# Run it before cutting a release (part of the #6 checklist); wire into a
# pre-commit hook or CI if desired.

set -eu

cd "$(dirname "$0")/.."

if [ $# -eq 2 ]; then
  xml=$1
  txt=$2
else
  xml=$(sed -n 's/^ *"xml": *"\(.*\)".*/\1/p' manifest.json)
  txt=$(sed -n 's/^ *"txt": *"\(.*\)".*/\1/p' manifest.json)
fi

[ -f "$xml" ] || { echo "parity FAIL: missing $xml (check manifest.json)"; exit 1; }
[ -f "$txt" ] || { echo "parity FAIL: missing $txt (check manifest.json)"; exit 1; }
grep -q '^<?xml' "$txt" || { echo "parity FAIL: no <?xml line in $txt — preamble must be followed by the full XML body"; exit 1; }

# The .txt body is everything from its "<?xml" line onward.
if awk '/^<\?xml/{f=1} f' "$txt" | diff -u - "$xml"; then
  echo "parity OK: $xml matches the $txt body"
else
  echo "parity FAIL: $xml and $txt have drifted (diff above; '-' is the .txt body)."
  echo "Versions ship in sync — apply every script edit to BOTH files;"
  echo "only the .txt usage preamble may differ."
  exit 1
fi
