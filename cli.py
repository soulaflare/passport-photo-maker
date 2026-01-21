#!/usr/bin/env python3
import io
import os
import sys
from PIL import Image

import tkinter as tk
from tkinter import filedialog, messagebox

# Target physical size (mm) and resolution (dpi)
MM_WIDTH = 35
MM_HEIGHT = 45
DPI = 300
MAX_BYTES = 1 * 1024 * 1024  # 1 MB

# Convert mm to pixels at given DPI
def mm_to_pixels(mm, dpi=DPI):
    inches = mm / 25.4
    return round(inches * dpi)

TARGET_WIDTH_PX = mm_to_pixels(MM_WIDTH)
TARGET_HEIGHT_PX = mm_to_pixels(MM_HEIGHT)
TARGET_RATIO = MM_WIDTH / MM_HEIGHT  # 7:9 ≈ 0.777...


def center_crop_to_ratio(img, target_ratio):
    """Center-crop the image to the target aspect ratio (width/height)."""
    w, h = img.size
    current_ratio = w / h

    if abs(current_ratio - target_ratio) < 1e-3:
        # Already the right ratio
        return img

    if current_ratio > target_ratio:
        # Image is too wide: crop width
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        right = left + new_w
        top = 0
        bottom = h
    else:
        # Image is too tall: crop height
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        bottom = top + new_h
        left = 0
        right = w

    return img.crop((left, top, right, bottom))


def save_jpeg_under_size(img, out_path, max_bytes=MAX_BYTES, dpi=DPI):
    """
    Save JPEG trying to stay under max_bytes.
    Uses binary search on 'quality' between 30 and 95.
    """
    low_q = 30
    high_q = 95
    best_bytes = None
    best_data = None
    best_q = None

    while low_q <= high_q:
        q = (low_q + high_q) // 2
        buffer = io.BytesIO()
        img.save(
            buffer,
            format="JPEG",
            dpi=(dpi, dpi),
            quality=q,
            optimize=True,
            progressive=True,
        )
        size = buffer.tell()

        if size <= max_bytes:
            # This quality works; try higher for better quality
            best_bytes = size
            best_data = buffer.getvalue()
            best_q = q
            low_q = q + 1
        else:
            # Too large; go lower quality
            high_q = q - 1

    if best_data is None:
        # Even lowest quality didn't fit; save at lowest quality anyway
        buffer = io.BytesIO()
        img.save(
            buffer,
            format="JPEG",
            dpi=(dpi, dpi),
            quality=low_q,
            optimize=True,
            progressive=True,
        )
        best_data = buffer.getvalue()
        best_bytes = len(best_data)
        best_q = low_q
        messagebox.showwarning(
            "Warning",
            (
                f"Could not get under {max_bytes} bytes.\n\n"
                f"Saved at quality={best_q} with size={best_bytes} bytes."
            ),
        )
    else:
        # Optional: you can print or log these
        print(
            f"Saved under {max_bytes} bytes. "
            f"Chosen quality={best_q}, size={best_bytes} bytes."
        )

    with open(out_path, "wb") as f:
        f.write(best_data)


def process_image(input_path, output_path):
    img = Image.open(input_path)

    # Convert to RGB to avoid issues with PNG/alpha, etc.
    if img.mode != "RGB":
        img = img.convert("RGB")

    # 1. Center-crop to correct aspect ratio (35x45 mm → 7:9)
    img = center_crop_to_ratio(img, TARGET_RATIO)

    # 2. Resize to exact pixel dimensions for 35x45 mm @ 300 dpi
    img = img.resize((TARGET_WIDTH_PX, TARGET_HEIGHT_PX), Image.LANCZOS)

    # 3. Save as compressed JPEG under 1 MB
    save_jpeg_under_size(img, output_path, MAX_BYTES, DPI)


def main():
    # Create hidden root window for dialogs
    root = tk.Tk()
    root.withdraw()
    root.update()

    # 1. Ask user to select input image
    input_path = filedialog.askopenfilename(
        title="Select input photo",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
            ("All files", "*.*"),
        ],
    )

    if not input_path:
        # User cancelled
        root.destroy()
        sys.exit(0)

    # 2. Suggest default output path
    folder, filename = os.path.split(input_path)
    name, _ext = os.path.splitext(filename)
    default_output = os.path.join(folder, name + "_passport.jpg")

    output_path = filedialog.asksaveasfilename(
        title="Save passport photo as...",
        initialdir=folder,
        initialfile=os.path.basename(default_output),
        defaultextension=".jpg",
        filetypes=[("JPEG image", "*.jpg *.jpeg")],
    )

    if not output_path:
        # User cancelled save dialog
        root.destroy()
        sys.exit(0)

    try:
        process_image(input_path, output_path)
        messagebox.showinfo(
            "Done",
            (
                f"Passport photo created.\n\n"
                f"Saved to:\n{output_path}\n\n"
                f"Size: {MM_WIDTH} x {MM_HEIGHT} mm @ {DPI} dpi\n"
                f"Pixels: {TARGET_WIDTH_PX} x {TARGET_HEIGHT_PX}"
            ),
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n\n{e}")

    root.destroy()


if __name__ == "__main__":
    main()