"""
Send Button Reference Image Capture Tool
Captures reference images of the send button in different states
"""

import pyautogui
import keyboard
import os
import config
from datetime import datetime


def capture_send_button_state(state_name):
    """
    Capture the send button in a specific state
    
    Args:
        state_name: Name of the state (e.g., 'ready', 'sent')
    """
    # Define send button region (same as used in automation)
    send_region = (
        config.GEMINI_SEND_BUTTON['x'] - 30,
        config.GEMINI_SEND_BUTTON['y'] - 30,
        60,
        60
    )
    
    print(f"\n{'='*60}")
    print(f"Capturing Send Button State: {state_name.upper()}")
    print(f"{'='*60}")
    print(f"\nRegion: x={send_region[0]}, y={send_region[1]}, "
          f"width={send_region[2]}, height={send_region[3]}")
    print(f"\nPosition the send button in the '{state_name}' state")
    print("Press SPACEBAR when ready to capture...")
    
    # Wait for spacebar
    keyboard.wait('space')
    
    # Capture the region
    screenshot = pyautogui.screenshot(region=send_region)
    
    # Create reference_images directory if it doesn't exist
    ref_dir = 'reference_images'
    if not os.path.exists(ref_dir):
        os.makedirs(ref_dir)
    
    # Save the image
    filename = f"{ref_dir}/send_button_{state_name}.png"
    screenshot.save(filename)
    
    print(f"\n✓ Captured and saved to: {filename}")
    print(f"  Image size: {screenshot.size}")
    
    return filename


def main():
    """Main function"""
    print("\n" + "="*60)
    print("Send Button Reference Image Capture Tool")
    print("="*60)
    print("\nThis tool will help you capture reference images of the")
    print("send button in different states for accurate detection.")
    print("\nMake sure Gemini is open and visible on your screen!")
    print("="*60)
    
    input("\nPress ENTER to continue...")
    
    # Capture state 1: Send button ready (after image upload)
    print("\n\n" + "="*60)
    print("STATE 1: SEND BUTTON READY")
    print("="*60)
    print("\nInstructions:")
    print("1. Paste an image into Gemini chat")
    print("2. Wait for the image to finish uploading")
    print("3. The send button should be READY to click (enabled)")
    print("4. Press SPACEBAR to capture")
    
    capture_send_button_state('ready')
    
    # Capture state 2: Message sent (blue stop square visible)
    print("\n\n" + "="*60)
    print("STATE 2: MESSAGE SENT")
    print("="*60)
    print("\nInstructions:")
    print("1. Click the send button to send the message")
    print("2. Wait for the blue STOP square to appear")
    print("3. The button should show the stop symbol")
    print("4. Press SPACEBAR to capture")
    
    capture_send_button_state('sent')
    
    # Summary
    print("\n\n" + "="*60)
    print("✓ CAPTURE COMPLETE!")
    print("="*60)
    print("\nReference images saved:")
    print("  • reference_images/send_button_ready.png")
    print("  • reference_images/send_button_sent.png")
    print("\nThese images will be used for send button detection.")
    print("You can re-run this script anytime to update the references.")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCapture cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
