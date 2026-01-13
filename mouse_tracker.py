"""
Mouse Coordinate Tracker
Simple tool to display current mouse position in real-time
Useful for finding exact coordinates for calibration
"""

import pyautogui
import time
import sys

def track_mouse():
    """Display mouse coordinates in real-time"""
    print("=" * 60)
    print("Mouse Coordinate Tracker")
    print("=" * 60)
    print("\nMove your mouse around to see coordinates")
    print("Press Ctrl+C to exit")
    print("\n" + "=" * 60 + "\n")
    
    try:
        prev_pos = None
        while True:
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Only print if position changed (reduces spam)
            if (x, y) != prev_pos:
                # Clear line and print new position
                print(f"\rMouse Position: X={x:4d}, Y={y:4d}  ", end='', flush=True)
                prev_pos = (x, y)
            
            time.sleep(0.1)  # Check 10 times per second
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Tracker stopped.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    track_mouse()
