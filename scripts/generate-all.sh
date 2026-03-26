#!/bin/bash
# Regenerate all website screenshots using device bezels.
# Run from anywhere: ./scripts/generate-all.sh
#
# On first run, creates a local .venv and installs dependencies automatically.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
PSD="$HOME/projects/apple/Bezel-iPhone-17/Photoshop/iPhone 17 Pro Max/iPhone 17 Pro Max - Deep Blue - Portrait.psd"
IPAD_PSD="$HOME/projects/apple/Bezel-iPad-Pro-M4/Photoshop/iPad Pro 13 - M4 - Space Gray - Portrait.psd"
IOS_SHOTS="$HOME/projects/banderly/banderly-ios/docs/screenshots/iphone/light"
IPAD_SHOTS="$HOME/projects/banderly/banderly-ios/docs/screenshots/ipad/light"
ANDROID_SHOTS="$HOME/projects/banderly/banderly-flutter/docs/screenshots/phone/light"

# --- Set up venv with dependencies if needed ---
if [ ! -f "$VENV_DIR/bin/python3" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

if ! "$VENV_DIR/bin/python3" -c "import numpy, PIL, psd_tools" 2>/dev/null; then
    echo "Installing dependencies..."
    "$VENV_DIR/bin/pip" install --quiet Pillow psd-tools numpy
fi

PYTHON="$VENV_DIR/bin/python3"

# --- Generate iOS screenshots ---
echo "=== iOS (iPhone 17 Pro Max) ==="
"$PYTHON" "$SCRIPT_DIR/generate-screenshot.py" "$IOS_SHOTS/04-home-dashboard.png"      "$PSD" screenshot-home
"$PYTHON" "$SCRIPT_DIR/generate-screenshot.py" "$IOS_SHOTS/06-songs-list.png"           "$PSD" screenshot-songs
"$PYTHON" "$SCRIPT_DIR/generate-screenshot.py" "$IOS_SHOTS/09-song-editor-populated.png" "$PSD" screenshot-song-editor
"$PYTHON" "$SCRIPT_DIR/generate-screenshot.py" "$IOS_SHOTS/11-setlists.png"             "$PSD" screenshot-setlists
"$PYTHON" "$SCRIPT_DIR/generate-screenshot.py" "$IOS_SHOTS/13-setlist-builder.png"      "$PSD" screenshot-setlist-detail
"$PYTHON" "$SCRIPT_DIR/generate-screenshot.py" "$IOS_SHOTS/15-performance.png"          "$PSD" screenshot-perform

# --- Generate Android screenshots ---
echo ""
echo "=== Android (Pixel 7) ==="
"$PYTHON" "$SCRIPT_DIR/generate-android-screenshot.py" "$ANDROID_SHOTS/04-home-dashboard.png"      screenshot-android-home
"$PYTHON" "$SCRIPT_DIR/generate-android-screenshot.py" "$ANDROID_SHOTS/06-songs-list.png"           screenshot-android-songs
"$PYTHON" "$SCRIPT_DIR/generate-android-screenshot.py" "$ANDROID_SHOTS/09-song-editor-populated.png" screenshot-android-song-editor
"$PYTHON" "$SCRIPT_DIR/generate-android-screenshot.py" "$ANDROID_SHOTS/11-setlists.png"             screenshot-android-setlists
"$PYTHON" "$SCRIPT_DIR/generate-android-screenshot.py" "$ANDROID_SHOTS/13-setlist-builder.png"      screenshot-android-setlist-detail
"$PYTHON" "$SCRIPT_DIR/generate-android-screenshot.py" "$ANDROID_SHOTS/15-performance.png"          screenshot-android-perform

# --- Generate iPad screenshots ---
echo ""
echo "=== iPad (iPad Pro 13 M4) ==="
"$PYTHON" "$SCRIPT_DIR/generate-ipad-screenshot.py" "$IPAD_SHOTS/04-home-dashboard.png"      "$IPAD_PSD" screenshot-ipad-home
"$PYTHON" "$SCRIPT_DIR/generate-ipad-screenshot.py" "$IPAD_SHOTS/06-songs-list.png"           "$IPAD_PSD" screenshot-ipad-songs
"$PYTHON" "$SCRIPT_DIR/generate-ipad-screenshot.py" "$IPAD_SHOTS/09-song-editor-populated.png" "$IPAD_PSD" screenshot-ipad-song-editor
"$PYTHON" "$SCRIPT_DIR/generate-ipad-screenshot.py" "$IPAD_SHOTS/11-setlists.png"             "$IPAD_PSD" screenshot-ipad-setlists
"$PYTHON" "$SCRIPT_DIR/generate-ipad-screenshot.py" "$IPAD_SHOTS/13-setlist-builder.png"      "$IPAD_PSD" screenshot-ipad-setlist-detail
"$PYTHON" "$SCRIPT_DIR/generate-ipad-screenshot.py" "$IPAD_SHOTS/15-performance.png"          "$IPAD_PSD" screenshot-ipad-perform

echo ""
echo "All screenshots generated."
