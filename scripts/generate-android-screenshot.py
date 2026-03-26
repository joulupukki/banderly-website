#!/usr/bin/env python3
"""
Generate Android mockup screenshots from app screenshots and Pixel 7 SDK skin.

Usage:
    python3 scripts/generate-android-screenshot.py <screenshot.png> <output_name>

Outputs:
    public/images/<output_name>-full.png   - Full-resolution (transparent PNG)
    public/images/<output_name>.png        - Web-optimized (max 800px wide, transparent PNG)

Uses the Pixel 7 skin from the Android SDK:
    ~/Library/Android/sdk/skins/pixel_7/

Requirements:
    pip install Pillow numpy
"""

import sys
import os
import numpy as np
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "public", "images")

SKIN_DIR = os.path.expanduser("~/Library/Android/sdk/skins/pixel_7")
BACK_PATH = os.path.join(SKIN_DIR, "back.webp")
MASK_PATH = os.path.join(SKIN_DIR, "mask.webp")

# From the layout file: screen offset within the bezel frame
SCREEN_X = 59
SCREEN_Y = 58
SCREEN_W = 1080
SCREEN_H = 2400
FRAME_W = 1200
FRAME_H = 2541

WEB_MAX_WIDTH = 800

# Status bar height on Pixel 7 (1080x2400 at 420dpi) — 24dp * 2.625 scale
STATUS_BAR_PX = 63

# Height of the gradient blend zone below the blanked status bar
BLEND_HEIGHT = 30


def composite(screenshot_path):
    """Composite a screenshot into the Pixel 7 bezel frame."""

    # Load bezel frame and mask
    frame = Image.open(BACK_PATH).convert("RGBA")
    mask = Image.open(MASK_PATH).convert("RGBA")

    # Load and resize screenshot to screen dimensions
    screenshot = Image.open(screenshot_path).convert("RGBA")
    screenshot = screenshot.resize((SCREEN_W, SCREEN_H), Image.LANCZOS)
    shot_arr = np.array(screenshot)

    # Blank the Android status bar and replace with background color
    if STATUS_BAR_PX > 0:
        sample_y_start = STATUS_BAR_PX + 20
        sample_y_end = min(sample_y_start + 10, SCREEN_H)
        sample_strip = shot_arr[sample_y_start:sample_y_end, :, :3]
        bg_color = np.median(sample_strip, axis=(0, 1)).astype(np.uint8)

        shot_arr[:STATUS_BAR_PX, :, 0] = bg_color[0]
        shot_arr[:STATUS_BAR_PX, :, 1] = bg_color[1]
        shot_arr[:STATUS_BAR_PX, :, 2] = bg_color[2]
        shot_arr[:STATUS_BAR_PX, :, 3] = 255

        # Soft gradient blend into real content
        blend_end = min(STATUS_BAR_PX + BLEND_HEIGHT, SCREEN_H)
        for y in range(STATUS_BAR_PX, blend_end):
            t = (y - STATUS_BAR_PX) / BLEND_HEIGHT
            shot_arr[y, :, 0] = (bg_color[0] * (1 - t) + shot_arr[y, :, 0] * t).astype(np.uint8)
            shot_arr[y, :, 1] = (bg_color[1] * (1 - t) + shot_arr[y, :, 1] * t).astype(np.uint8)
            shot_arr[y, :, 2] = (bg_color[2] * (1 - t) + shot_arr[y, :, 2] * t).astype(np.uint8)

    # The SDK mask has alpha=255 at corners (cutout) and alpha=0 in the screen
    # area. Invert it to get: alpha=255 where the screen is visible.
    mask_arr = np.array(mask)
    screen_alpha = 255 - mask_arr[:, :, 3]
    shot_arr[:, :, 3] = np.minimum(shot_arr[:, :, 3], screen_alpha)

    # Composite: place screenshot behind the frame (frame has a transparent
    # hole where the screen is).
    prepared = Image.fromarray(shot_arr)
    result = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    result.paste(prepared, (SCREEN_X, SCREEN_Y), prepared)
    result = Image.alpha_composite(result, frame)

    # Trim to content bounding box
    bbox = result.getbbox()
    if bbox:
        result = result.crop(bbox)

    return result


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    screenshot_path = sys.argv[1]
    output_name = sys.argv[2]

    if not os.path.exists(screenshot_path):
        print(f"Error: Screenshot not found: {screenshot_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(BACK_PATH):
        print(f"Error: Pixel 7 skin not found: {SKIN_DIR}", file=sys.stderr)
        print("Install via Android Studio > SDK Manager > SDK Tools > Android Emulator", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Compositing {os.path.basename(screenshot_path)} into Pixel 7 frame...")
    result = composite(screenshot_path)

    # Save full-resolution PNG
    full_path = os.path.join(OUTPUT_DIR, f"{output_name}-full.png")
    result.save(full_path, "PNG")
    print(f"  Full: {full_path} ({result.size[0]}x{result.size[1]})")

    # Save web-optimized PNG (scaled down)
    ratio = WEB_MAX_WIDTH / result.size[0]
    web_size = (WEB_MAX_WIDTH, int(result.size[1] * ratio))
    web = result.resize(web_size, Image.LANCZOS)
    web_path = os.path.join(OUTPUT_DIR, f"{output_name}.png")
    web.save(web_path, "PNG", optimize=True)
    print(f"  Web:  {web_path} ({web.size[0]}x{web.size[1]})")

    print("Done!")


if __name__ == "__main__":
    main()
