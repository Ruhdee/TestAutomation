"""
Quiz Automation Module
Contains all the automation functions for interacting with quiz and Gemini
Each function is independent and easy to modify
"""

import pyautogui
import pyperclip
import time
import re
from datetime import datetime
import os
import config

# Configure PyAutoGUI
pyautogui.PAUSE = config.PYAUTOGUI_PAUSE
pyautogui.FAILSAFE = config.PYAUTOGUI_FAILSAFE


class QuizAutomation:
    def __init__(self):
        self.question_count = 0
        self.setup_logging()
        
        # Screen shift detection
        self.screen_shift_region = (22, 454, 20, 20)  # x, y, width, height
        self.initial_screen_state = None
        self.screen_has_shifted = False
        
    def setup_logging(self):
        """Setup logging and screenshot directory"""
        if config.SAVE_SCREENSHOTS:
            os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        if config.DEBUG_MODE:
            with open(config.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
    
    def save_screenshot(self, name):
        """Save screenshot for debugging"""
        if config.SAVE_SCREENSHOTS:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{config.SCREENSHOT_DIR}/{timestamp}_{name}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            self.log(f"Screenshot saved: {filename}")
    
    def capture_question_screenshot(self):
        """
        Capture screenshot of question area instead of copying text
        EASY TO MODIFY: Adjust region in config.py
        """
        self.log("Capturing screenshot of question area...")
        
        # Capture the question area
        region = (
            config.QUIZ_QUESTION_AREA['x'],
            config.QUIZ_QUESTION_AREA['y'],
            config.QUIZ_QUESTION_AREA['width'],
            config.QUIZ_QUESTION_AREA['height']
        )
        
        screenshot = pyautogui.screenshot(region=region)
        
        # Save screenshot temporarily for pasting
        temp_path = f"{config.SCREENSHOT_DIR}/temp_question.png"
        os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
        screenshot.save(temp_path)
        
        self.log(f"Question screenshot saved to {temp_path}")
        
        # Also save for debugging
        if config.SAVE_SCREENSHOTS:
            debug_path = f"{config.SCREENSHOT_DIR}/question_{self.question_count}.png"
            screenshot.save(debug_path)
            self.log(f"Debug screenshot: {debug_path}")
        
        return temp_path
    
    def add_system_prompt_to_input(self):
        """
        Add system prompt before the image to remind Gemini of instructions
        This prevents Gemini from forgetting the rules
        """
        self.log("Adding system prompt to input...")
        
        # System prompt text (repeated with each question)
        system_prompt = (
            "TASK: Read the question from attached image. "
            "Answer with ONLY the letter (A, B, C, or D). "
            "Do NOT explain. Do NOT append to previous answers. "
            "Only answer the current question:\n\n"
        )
        
        # Type the system prompt
        pyperclip.copy(system_prompt)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)

    
    def paste_screenshot_to_gemini(self, screenshot_path):
        """
        Paste question screenshot into Gemini input field
        EASY TO MODIFY: Adjust coordinates in config.py
        """
        self.log("Pasting screenshot to Gemini...")
        
        # Load image to clipboard using PIL
        from PIL import Image
        import io
        
        # Open the image
        image = Image.open(screenshot_path)
        
        # Convert to clipboard format (Windows)
        output = io.BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # Remove BMP header
        output.close()
        
        # Copy image to clipboard (Windows specific)
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        self.log("Image copied to clipboard")
        
        # Click on Gemini input field
        pyautogui.click(
            config.GEMINI_INPUT_FIELD['x'],
            config.GEMINI_INPUT_FIELD['y']
        )
        time.sleep(config.DELAY_AFTER_CLICK)
        
        # Add system prompt first (to remind Gemini)
        self.add_system_prompt_to_input()
        
        # IMPORTANT: Reload image to clipboard (system prompt overwrote it)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        self.log("Image reloaded to clipboard")
        
        # Paste the image
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(config.DELAY_AFTER_PASTE)
        
        # Wait for image to upload by monitoring send button
        self.wait_for_send_button_ready()
        
        # Define send button region for verification
        send_region = (
            config.GEMINI_SEND_BUTTON['x'] - 30,
            config.GEMINI_SEND_BUTTON['y'] - 30,
            60,
            60
        )
        
        # Keep trying to click send button until change is detected
        max_attempts = 100000000
        click_successful = False
        
        for attempt in range(1, max_attempts + 1):
            # Take screenshot before clicking
            before_screenshot = pyautogui.screenshot(region=send_region)
            
            # Click the send button
            self.log(f"Clicking send button (attempt {attempt}/{max_attempts})...")
            pyautogui.click(
                config.GEMINI_SEND_BUTTON['x'],
                config.GEMINI_SEND_BUTTON['y']
            )
            time.sleep(0.3)
            
            # Move mouse away from button to avoid hover effect
            pyautogui.moveTo(
                config.GEMINI_SEND_BUTTON['x'] - 100,
                config.GEMINI_SEND_BUTTON['y']
            )
            time.sleep(0.2)
            
            # Verify the click worked by checking if screen changed
            after_screenshot = pyautogui.screenshot(region=send_region)
            similarity = self._get_similarity(before_screenshot, after_screenshot)
            
            if similarity > 0.95:  # Screen didn't change much
                self.log(f"  Attempt {attempt}: No change detected (similarity: {similarity:.2%})")
                if attempt < max_attempts:
                    self.log(f"  Retrying...")
                    time.sleep(0.5)
                else:
                    self.log(f"WARNING: Send button may not have been clicked after {max_attempts} attempts!")
            else:
                self.log(f"  Attempt {attempt}: Send button clicked successfully! (screen changed: {(1-similarity)*100:.1f}%)")
                click_successful = True
                break
        
        self.log("Screenshot sent to Gemini")
        self.save_screenshot(f"gemini_input_{self.question_count}")
    
    def wait_for_send_button_ready(self):
        """
        Wait for send button to become available after image upload
        Monitors send button area - button appearance changes when ready
        """
        self.log("Waiting for image to upload (monitoring send button)...")
        time.sleep(1.0)  # Initial delay for upload to start
        
        max_wait_time = 10  # Maximum 10 seconds
        check_interval = 0.5  # Check every 0.5 seconds
        elapsed_time = 1.0
        
        # Define send button area to monitor
        button_region = (
            config.GEMINI_SEND_BUTTON['x'] - 30,
            config.GEMINI_SEND_BUTTON['y'] - 30,
            80,
            80
        )
        
        # Take initial screenshot
        prev_screenshot = pyautogui.screenshot(region=button_region)
        stable_count = 0
        
        while elapsed_time < max_wait_time:
            time.sleep(check_interval)
            elapsed_time += check_interval
            
            # Take new screenshot
            curr_screenshot = pyautogui.screenshot(region=button_region)
            
            # Check if button appearance has stabilized (upload complete)
            if self._images_similar(prev_screenshot, curr_screenshot, threshold=0.98):
                stable_count += 1
                if stable_count >= 3:  # Stable for 1.5 seconds
                    self.log(f"Send button ready after {elapsed_time:.1f}s")
                    return
            else:
                stable_count = 0  # Reset if still changing
            
            prev_screenshot = curr_screenshot
        
        # Timeout - proceed anyway
        self.log(f"Send button timeout after {elapsed_time:.1f}s, proceeding anyway")

    
    def wait_for_gemini_processing(self):
        """
        Wait for Gemini to finish processing by polling for valid answer
        Repeatedly selects text from response area until valid answer (A/B/C/D) is found
        """
        self.log("Waiting for Gemini response...")
        time.sleep(2.0)  # Initial delay for processing to start
        
        max_attempts = 40  # Maximum 40 attempts (20 seconds at 0.5s intervals)
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            time.sleep(0.5)
            
            # Try to get response
            response = self._try_get_response()
            
            # Check if we got a valid answer
            if response and self._is_valid_answer(response):
                self.log(f"Valid response found after {attempt * 0.5:.1f}s: '{response}'")
                return response
            else:
                if attempt % 4 == 0:  # Log every 2 seconds
                    self.log(f"  [{attempt * 0.5:.1f}s] Waiting for valid response... (got: '{response}')")
        
        self.log(f"WARNING: No valid response after {max_attempts * 0.5:.1f}s")
        return None
    
    def _try_get_response(self):
        """
        Try to select and copy text from Gemini response area
        Selects from bottom-right to top-left to avoid Analysis dropdown
        """
        try:
            # Calculate bottom-right position
            bottom_right_x = config.GEMINI_RESPONSE_AREA['x'] + config.GEMINI_RESPONSE_AREA['width'] - 5
            bottom_right_y = config.GEMINI_RESPONSE_AREA['y'] + config.GEMINI_RESPONSE_AREA['height'] - 5
            
            # Click at bottom-right and triple-click to select
            pyautogui.click(bottom_right_x, bottom_right_y, clicks=3)
            time.sleep(0.2)
            
            # Copy
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)
            
            # Get from clipboard
            response = pyperclip.paste().strip()
            return response
        except Exception as e:
            self.log(f"Error getting response: {e}")
            return None
    
    def _is_valid_answer(self, response):
        """Check if response contains a valid answer letter (A, B, C, or D)"""
        if not response:
            return False
        
        response_upper = response.upper()
        
        # Check if it's just the letter
        if response_upper in ['A', 'B', 'C', 'D']:
            return True
        
        # Check if it contains a valid letter
        import re
        match = re.search(r'\b([A-D])\b', response_upper)
        return match is not None
    
    def _get_similarity(self, img1, img2):
        """Get similarity percentage between two images"""
        import numpy as np
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        if arr1.shape != arr2.shape:
            return 0.0
        matches = np.sum(arr1 == arr2)
        total = arr1.size
        return matches / total
    
    def _images_similar(self, img1, img2, threshold=0.95):
        """
        Compare two images to see if they're similar
        Returns True if images are very similar (response has stopped changing)
        """
        import numpy as np
        
        # Convert to numpy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        
        # Calculate similarity (simple pixel comparison)
        if arr1.shape != arr2.shape:
            return False
        
        # Count matching pixels
        matches = np.sum(arr1 == arr2)
        total = arr1.size
        similarity = matches / total
        
        return similarity >= threshold
    
    def get_gemini_response(self):
        """
        Wait for and get Gemini's response
        Uses polling method - repeatedly tries to copy until valid answer found
        """
        # Wait for response and get it
        response = self.wait_for_gemini_processing()
        
        if response:
            self.log(f"Gemini response (length: {len(response)}): '{response}'")
        else:
            self.log("WARNING: Empty or invalid response from Gemini!")
            self.log(f"Response area configured as: x={config.GEMINI_RESPONSE_AREA['x']}, "
                     f"y={config.GEMINI_RESPONSE_AREA['y']}, "
                     f"width={config.GEMINI_RESPONSE_AREA['width']}, "
                     f"height={config.GEMINI_RESPONSE_AREA['height']}")
            self.log("TIP: Run calibration.py again and select a LARGER response area")
            response = ""
        
        self.save_screenshot(f"gemini_response_{self.question_count}")
        
        return response
    
    def parse_answer(self, response):
        """
        Extract answer option from Gemini's response
        EASY TO MODIFY: Adjust parsing logic here
        """
        self.log(f"Parsing answer from: {response}")
        
        # Clean the response
        response = response.strip().upper()
        
        # Try to extract letter (A, B, C, D) or number (1, 2, 3, 4)
        if config.EXPECTED_ANSWER_FORMAT == 'letter':
            # Look for A, B, C, or D
            match = re.search(r'\b([A-D])\b', response)
            if match:
                answer = match.group(1)
                self.log(f"Extracted answer: {answer}")
                return answer
            # If response is just the letter
            if response in ['A', 'B', 'C', 'D']:
                self.log(f"Direct answer: {response}")
                return response
        
        elif config.EXPECTED_ANSWER_FORMAT == 'number':
            # Look for 1, 2, 3, or 4
            match = re.search(r'\b([1-4])\b', response)
            if match:
                number = match.group(1)
                # Convert to letter
                answer = chr(64 + int(number))  # 1->A, 2->B, etc.
                self.log(f"Extracted answer: {number} -> {answer}")
                return answer
        
        # Fallback: try to find first letter
        for char in response:
            if char in ['A', 'B', 'C', 'D']:
                self.log(f"Fallback extracted: {char}")
                return char
        
        self.log("WARNING: Could not parse answer! Defaulting to A")
        return 'A'  # Default fallback
    
    def select_answer(self, option):
        """
        Click on the correct answer option
        Uses Q1 coordinates if screen hasn't shifted, Q2+ if it has
        EASY TO MODIFY: Adjust option coordinates in config.py
        """
        self.log(f"Selecting answer: {option}")
        
        # Choose coordinate set based on screen shift status
        if not self.screen_has_shifted:
            answer_coords = config.ANSWER_OPTIONS_Q1
            coord_type = "Q1"
        else:
            answer_coords = config.ANSWER_OPTIONS_Q2
            coord_type = "Q2+"
        
        if option not in answer_coords:
            self.log(f"ERROR: Invalid option {option}")
            return False
        
        self.log(f"Using {coord_type} coordinates for question #{self.question_count}")
        
        # Click on the answer option
        pyautogui.click(
            answer_coords[option]['x'],
            answer_coords[option]['y']
        )
        time.sleep(config.DELAY_AFTER_CLICK)
        
        self.log(f"Answer {option} selected")
        self.save_screenshot(f"answer_selected_{self.question_count}")
        
        return True
    
    def click_next(self):
        """
        Click the next button to move to next question
        Detects screen shift dynamically to use appropriate coordinates
        EASY TO MODIFY: Adjust button coordinates in config.py
        """
        self.log("Clicking next button...")
        
        # For question 1, capture screen state BEFORE clicking next
        if self.question_count == 1 and self.initial_screen_state is None:
            self.initial_screen_state = pyautogui.screenshot(region=self.screen_shift_region)
            self.log(f"Captured initial screen state (before clicking next) at region {self.screen_shift_region}")
        
        # Choose coordinate based on screen shift status
        if not self.screen_has_shifted:
            next_coords = config.NEXT_BUTTON_Q1
            coord_type = "Q1"
        else:
            next_coords = config.NEXT_BUTTON_Q2
            coord_type = "Q2+"
        
        self.log(f"Using {coord_type} coordinates for question #{self.question_count}")
        
        pyautogui.click(
            next_coords['x'],
            next_coords['y']
        )
        time.sleep(config.DELAY_BETWEEN_QUESTIONS)
        
        self.log("Moved to next question")
        self.save_screenshot(f"next_question_{self.question_count}")
        
        # After first question, check if screen has shifted
        if self.question_count == 1:
            self.check_screen_shift()
    
    def check_screen_shift(self):
        """
        Check if the screen has shifted by comparing a specific region
        Region: x=22-42, y=454-474 (20x20 pixels)
        Compares screen state before and after clicking next on question 1
        Once shifted, stays shifted for all remaining questions
        """
        # Compare current state (after clicking next) with initial state (before clicking next)
        time.sleep(0.5)  # Wait for screen to settle
        current_state = pyautogui.screenshot(region=self.screen_shift_region)
        similarity = self._get_similarity(self.initial_screen_state, current_state)
        
        if similarity < 0.95:  # Screen has changed (shifted)
            self.screen_has_shifted = True
            self.log(f"Screen shift DETECTED! (similarity: {similarity:.2%}) - Switching to Q2+ coordinates permanently")
        else:
            # Don't set to False - keep using Q1 coordinates
            self.log(f"No screen shift detected (similarity: {similarity:.2%}) - Continuing with Q1 coordinates")
    
    def process_question(self):
        """
        Process a single question - main workflow
        Returns True if successful, False if should stop
        """
        self.question_count += 1
        self.log(f"\n{'='*60}")
        self.log(f"Processing Question #{self.question_count}")
        self.log(f"{'='*60}")
        
        try:
            # Step 1: Capture screenshot of question
            screenshot_path = self.capture_question_screenshot()
            
            # Step 2: Paste screenshot to Gemini
            self.paste_screenshot_to_gemini(screenshot_path)
            
            # Step 3: Wait for and get Gemini's response
            response = self.get_gemini_response()
            
            # Step 4: Parse the answer
            answer = self.parse_answer(response)
            
            # Step 5: Select the answer
            self.select_answer(answer)
            
            # Step 6: Click next
            self.click_next()
            
            self.log(f"Question #{self.question_count} completed successfully")
            return True
            
        except Exception as e:
            self.log(f"ERROR processing question: {str(e)}")
            self.save_screenshot(f"error_{self.question_count}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
            return False
