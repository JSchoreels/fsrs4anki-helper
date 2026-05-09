#!/usr/bin/env bash
set -euo pipefail

ADDON_DIR="${1:-.}"
OUT_DIR="${2:-.}"
ADDON_NAME="fsrs4anki-helper"

if [[ ! -d "$ADDON_DIR" ]]; then
    echo "Addon dir not found: $ADDON_DIR" >&2
    exit 1
fi

for required_file in manifest.json __init__.py config.json config.md; do
    if [[ ! -f "$ADDON_DIR/$required_file" ]]; then
        echo "$required_file not found in $ADDON_DIR" >&2
        exit 1
    fi
done

mkdir -p "$OUT_DIR"
OUT_DIR_ABS=$(cd "$OUT_DIR" && pwd)
OUT_FILE="$OUT_DIR_ABS/${ADDON_NAME}.ankiaddon"

rm -f "$OUT_FILE"

(
    cd "$ADDON_DIR"
    zip -q -X -r "$OUT_FILE" \
        __init__.py \
        utils.py \
        fsrs_math.py \
        dsr_state.py \
        sync_hook.py \
        stats.py \
        configuration.py \
        i18n.py \
        steps.py \
        browser/browser.py \
        browser/custom_columns.py \
        browser/sort_order.py \
        schedule/ \
        locale/ \
        python_i18n/i18n/ \
        manifest.json \
        README.md \
        License \
        config.json \
        config.md \
        -x "*/.git" \
        -x "*/.git/*" \
        -x "*/__pycache__/*" \
        -x "python_i18n/i18n/tests/*" \
        -x "*.pyc" \
        -x "*.pyo" \
        -x "*.DS_Store"
)

echo "Wrote $OUT_FILE"
