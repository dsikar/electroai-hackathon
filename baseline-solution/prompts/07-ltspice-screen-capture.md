Perfect — here's the cleanest, most reliable way to automate this on Linux + Wine.
LTSpice itself has no built-in command-line image export for schematics (only simulation batch mode via -b), so the standard approach is:

Launch LTSpice via Wine with the .asc file as argument (it opens the schematic directly).
Use Linux tools (xdotool + import from ImageMagick) to focus the window, zoom-to-fit, and capture a clean screenshot.
Save the PNG right next to the .asc with the same base name.

This is fully scriptable and works great in pipelines.
1. Install dependencies (once)
Bashsudo apt update
sudo apt install xdotool imagemagick
2. Ready-to-use Bash script
Save this as ltspice_screenshot.sh:
Bash#!/bin/bash
# ================================================
# LTSpice Auto-Screenshot on Linux + Wine
# Usage: ./ltspice_screenshot.sh /path/to/circuit.asc
#        (or pass multiple files)
# ================================================

set -euo pipefail

# === CHANGE THIS TO MATCH YOUR LTSPICE INSTALL ===
LTSPICE_EXE="$HOME/.wine/drive_c/Program Files/LTC/LTspiceXVII/XVIIx64.exe"
# Common alternatives:
# LTSPICE_EXE="$HOME/.wine/drive_c/Program Files (x86)/LTC/LTspiceXVII/XVIIx64.exe"
# LTSPICE_EXE="$HOME/.wine/drive_c/Program Files/LTC/LTspiceIV/scad3.exe"

if [ ! -f "$LTSPICE_EXE" ]; then
    echo "❌ LTSpice executable not found at: $LTSPICE_EXE"
    echo "   Please edit the LTSPICE_EXE path in the script."
    exit 1
fi

process_file() {
    local ASC_FILE="$(realpath "$1")"
    if [ ! -f "$ASC_FILE" ]; then
        echo "❌ File not found: $ASC_FILE"
        return 1
    fi

    local DIR="$(dirname "$ASC_FILE")"
    local BASE="$(basename "$ASC_FILE" .asc)"
    local PNG_FILE="$DIR/$BASE.png"

    echo "🚀 Launching LTSpice → $ASC_FILE"

    # Launch (background)
    wine "$LTSPICE_EXE" "$ASC_FILE" &
    local LTSPICE_PID=$!

    # Wait for window (LTspice window title usually contains "LTspice")
    echo "   Waiting for window..."
    local WINID=""
    for i in {1..30}; do
        WINID=$(xdotool search --name "LTspice" --onlyvisible 2>/dev/null | tail -n1 || true)
        if [ -n "$WINID" ]; then
            break
        fi
        sleep 0.5
    done

    if [ -z "$WINID" ]; then
        echo "❌ Could not detect LTSpice window. Killing process."
        kill "$LTSPICE_PID" 2>/dev/null || true
        return 1
    fi

    echo "   Window found (ID $WINID) — preparing screenshot..."

    # Focus, maximize, zoom-to-fit (Space key in LTSpice)
    xdotool windowactivate --sync "$WINID" 2>/dev/null || true
    sleep 1.2
    xdotool windowstate --add MAXIMIZED "$WINID" 2>/dev/null || true
    sleep 0.8
    xdotool key --window "$WINID" space  # Zoom to Fit
    sleep 1.0

    # Capture clean screenshot of the LTSpice window
    import -window "$WINID" -quality 95 -strip "$PNG_FILE"

    echo "✅ Screenshot saved → $PNG_FILE"

    # Optional: auto-close LTSpice after screenshot (uncomment if you want)
    # xdotool windowkill "$WINID" 2>/dev/null || kill "$LTSPICE_PID" 2>/dev/null || true
}

# Process all files passed as arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1.asc> [file2.asc ...]"
    exit 1
fi

for file in "$@"; do
    process_file "$file"
done

echo "🎉 All done!"
How to use it in your pipeline
Bashchmod +x ltspice_screenshot.sh

# Single file
./ltspice_screenshot.sh /path/to/your/circuit.asc

# Multiple files (perfect for your 2 circuit files)
./ltspice_screenshot.sh circuitA.asc circuitB.asc
The PNGs will appear right next to the .asc files (e.g. circuitA.png).
Tips & tweaks

Window detection works reliably because LTSpice window titles contain “LTspice”.
Timing is tuned for typical machines — increase the sleep values if your system is slow.
Want it in Python? (like your Falstad script) — just say the word and I’ll give you the subprocess + xdotool equivalent.
Headless/CI? This works on servers with Xvfb if needed (xvfb-run ./ltspice_screenshot.sh ...).

Bonus (even cleaner, no Wine)
If you ever want zero GUI dependency, use ltspice2svg (native Linux binary). It converts .asc → publication-quality SVG instantly, then you can turn it into PNG with rsvg-convert. Many people use it for exactly this purpose. Let me know if you want that version instead.
Drop the script in, point it at your two .asc files after your pipeline runs, and you’re fully automated.
Need any tweaks (different zoom level, crop the toolbar, batch mode changes, etc.)? Just tell me!
