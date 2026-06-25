#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 OUTPUT_DIR ZIP1 ZIP2 [ZIP3 ...]"
  exit 1
fi

OUT="$1"
shift
WORK="$(mktemp -d)"
REPORT="$OUT/MERGE_REPORT.txt"
rm -rf "$OUT"
mkdir -p "$OUT"
: > "$REPORT"

for ZIP in "$@"; do
  NAME="$(basename "$ZIP")"
  TMP="$WORK/${NAME%.zip}"
  mkdir -p "$TMP"
  unzip -q "$ZIP" -d "$TMP"
  ROOT="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -1)"
  echo "== MERGE $NAME root=$(basename "$ROOT") ==" >> "$REPORT"
  while IFS= read -r -d '' SRC; do
    REL="${SRC#"$ROOT"/}"
    DEST="$OUT/$REL"
    if [ -e "$DEST" ]; then
      if [ -f "$SRC" ] && [ -f "$DEST" ] && cmp -s "$SRC" "$DEST"; then
        echo "same: $REL" >> "$REPORT"
      else
        echo "overwrite: $REL by $NAME" >> "$REPORT"
      fi
    fi
    mkdir -p "$(dirname "$DEST")"
    cp -a "$SRC" "$DEST"
  done < <(find "$ROOT" -mindepth 1 -print0)
done

echo "Merged into: $OUT"
echo "Report: $REPORT"
