#!/usr/bin/env python3
"""
Generate iPad mockup screenshots from app screenshots and Apple PSD bezels.

Usage:
    python3 scripts/generate-ipad-screenshot.py <screenshot.png> <bezel.psd> <output_name>

Outputs:
    public/images/<output_name>.png        - Web-optimized (max 800px wide, transparent PNG)
    public/images/<output_name>-full.png   - Full-resolution (transparent PNG)

Requirements:
    pip install Pillow psd-tools numpy

Example:
    python3 scripts/generate-ipad-screenshot.py \
        "/path/to/screenshot.png" \
        "/path/to/iPad Pro 13 - M4 - Space Gray - Portrait.psd" \
        screenshot-ipad-home
"""

import sys
import os
import numpy as np
from PIL import Image
from psd_tools import PSDImage

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "public", "images")

WEB_MAX_WIDTH = 800

# How far below the Status Bar bottom edge to sample the background color,
# and the height of the gradient blend zone (in screen-relative pixels).
BG_SAMPLE_OFFSET = 20
BLEND_HEIGHT = 30

# The iPad PSD's "Status bars" layer is only 25px tall, but the actual
# status bar content in iPad screenshots extends further. This minimum
# ensures we blank enough to fully cover the screenshot's own status bar.
MIN_STATUS_BAR_HEIGHT = 50

# The iPad PSD uses "Status bars" (plural) instead of "Status Bar"
STATUS_BAR_LAYER_NAMES = ["Status Bar", "Status bars"]


def composite(screenshot_path, psd_path):
    """Composite a screenshot into the PSD iPad frame.

    The Apple iPad PSD has these layers (bottom to top):
      - Screen      — placeholder whose alpha defines the rounded-corner mask
      - Hardware    — the iPad bezel (smart object)
      - Status bars — Apple's canonical status bar

    Strategy:
      1. Blank out the screenshot's own status bar area and fill it with the
         screenshot's background color so there's no text clash.
      2. Use the Screen layer's alpha as a rounded-corner mask.
      3. Render the full PSD composite (including the Status Bar layer) and
         replace the gray screen placeholder with the prepared screenshot.
    """
    psd = PSDImage.open(psd_path)

    # --- Locate layers ---
    screen_layer = None
    status_bar_layer = None
    for layer in psd:
        if layer.name == "Screen":
            screen_layer = layer
        elif layer.name in STATUS_BAR_LAYER_NAMES:
            status_bar_layer = layer

    if screen_layer is None:
        print("Error: No 'Screen' layer found in PSD.", file=sys.stderr)
        sys.exit(1)

    sx, sy = screen_layer.left, screen_layer.top
    sw, sh = screen_layer.width, screen_layer.height

    # --- Calculate status bar region in screen-relative coordinates ---
    if status_bar_layer is not None:
        sb_top = status_bar_layer.top - sy
        sb_bottom = sb_top + status_bar_layer.height
    else:
        sb_top, sb_bottom = 0, 0

    # The area to blank: from the top of the screen down to the bottom
    # of the Status Bar layer (the PSD's status bar covers this zone).
    # Use MIN_STATUS_BAR_HEIGHT to ensure we cover the full screenshot status bar.
    blank_bottom = max(sb_bottom, MIN_STATUS_BAR_HEIGHT)

    # --- Extract the screen mask (rounded-corner alpha) ---
    screen_img = screen_layer.composite().convert("RGBA")
    screen_mask = np.array(screen_img)[:, :, 3]

    # --- Render the full PSD composite (WITH Status Bar included) ---
    full = psd.composite().convert("RGBA")
    full_arr = np.array(full)

    # --- Prepare the screenshot ---
    screenshot = Image.open(screenshot_path).convert("RGBA")
    screenshot = screenshot.resize((sw, sh), Image.LANCZOS)
    shot_arr = np.array(screenshot)

    # --- Blank out the screenshot's status bar area ---
    if blank_bottom > 0:
        # Sample the background color from a strip just below the status bar
        sample_y_start = blank_bottom + BG_SAMPLE_OFFSET
        sample_y_end = min(sample_y_start + 10, sh)
        # Use the median color of that strip (robust against UI elements)
        sample_strip = shot_arr[sample_y_start:sample_y_end, :, :3]
        bg_color = np.median(sample_strip, axis=(0, 1)).astype(np.uint8)

        # Fill the status bar zone with the background color
        shot_arr[:blank_bottom, :, 0] = bg_color[0]
        shot_arr[:blank_bottom, :, 1] = bg_color[1]
        shot_arr[:blank_bottom, :, 2] = bg_color[2]
        shot_arr[:blank_bottom, :, 3] = 255

        # Create a soft gradient blend from the filled area into the real content
        blend_end = min(blank_bottom + BLEND_HEIGHT, sh)
        for y in range(blank_bottom, blend_end):
            t = (y - blank_bottom) / BLEND_HEIGHT  # 0 at top, 1 at bottom
            shot_arr[y, :, 0] = (bg_color[0] * (1 - t) + shot_arr[y, :, 0] * t).astype(np.uint8)
            shot_arr[y, :, 1] = (bg_color[1] * (1 - t) + shot_arr[y, :, 1] * t).astype(np.uint8)
            shot_arr[y, :, 2] = (bg_color[2] * (1 - t) + shot_arr[y, :, 2] * t).astype(np.uint8)

    # Apply the screen layer's alpha as a mask (rounded corners)
    shot_arr[:, :, 3] = np.minimum(shot_arr[:, :, 3], screen_mask)

    # --- Build the final composite ---
    # Identify frame vs screen-placeholder pixels in the screen region
    screen_region_full = full_arr[sy : sy + sh, sx : sx + sw].copy()
    r = screen_region_full[:, :, 0].astype(float)
    g = screen_region_full[:, :, 1].astype(float)
    b = screen_region_full[:, :, 2].astype(float)
    gray_dist = np.sqrt((r - 127) ** 2 + (g - 127) ** 2 + (b - 127) ** 2)

    # Mask: 0 = screen placeholder, 1 = frame/status bar content
    frame_blend = np.clip((gray_dist - 2) / 13, 0, 1).astype(np.float32)

    # Blend screenshot with frame in the screen region
    for c in range(4):
        screen_region_full[:, :, c] = (
            shot_arr[:, :, c] * (1 - frame_blend)
            + screen_region_full[:, :, c] * frame_blend
        ).astype(np.uint8)

    # Assemble: frame outside screen region, blended content inside
    result_arr = full_arr.copy()
    result_arr[sy : sy + sh, sx : sx + sw] = screen_region_full

    result = Image.fromarray(result_arr)

    # Trim to content bounding box
    bbox = result.getbbox()
    if bbox:
        result = result.crop(bbox)

    return result


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    screenshot_path = sys.argv[1]
    psd_path = sys.argv[2]
    output_name = sys.argv[3]

    if not os.path.exists(screenshot_path):
        print(f"Error: Screenshot not found: {screenshot_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(psd_path):
        print(f"Error: PSD not found: {psd_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Compositing {os.path.basename(screenshot_path)} into iPad frame...")
    result = composite(screenshot_path, psd_path)

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
