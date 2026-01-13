"""
Interactive Calibration Tool for MCQ Quiz Automation
Run this script to easily capture screen coordinates for your quiz layout
"""

import pyautogui
import time
import sys
from pynput import mouse, keyboard as kb
from pynput.keyboard import Key, KeyCode

class CalibrationTool:
    def __init__(self):
        self.coordinates = {}
        self.current_step = 0
        self.running = True
        
        # Calibration steps
        self.steps = [
            {
                'name': 'QUIZ_QUESTION_AREA_TOP_LEFT',
                'instruction': 'Move mouse to TOP-LEFT corner of question area and press SPACE'
            },
            {
                'name': 'QUIZ_QUESTION_AREA_BOTTOM_RIGHT',
                'instruction': 'Move mouse to BOTTOM-RIGHT corner of question area and press SPACE'
            },
            # Question 1 coordinates
            {
                'name': 'ANSWER_A_Q1',
                'instruction': '[QUESTION 1] Click on answer option A and press SPACE'
            },
            {
                'name': 'ANSWER_B_Q1',
                'instruction': '[QUESTION 1] Click on answer option B and press SPACE'
            },
            {
                'name': 'ANSWER_C_Q1',
                'instruction': '[QUESTION 1] Click on answer option C and press SPACE'
            },
            {
                'name': 'ANSWER_D_Q1',
                'instruction': '[QUESTION 1] Click on answer option D and press SPACE'
            },
            {
                'name': 'NEXT_BUTTON_Q1',
                'instruction': '[QUESTION 1] Move mouse to NEXT button and press SPACE'
            },
            # Question 2+ coordinates (after screen shift)
            {
                'name': 'ANSWER_A_Q2',
                'instruction': '[QUESTION 2+] Click on answer option A (after screen shift) and press SPACE'
            },
            {
                'name': 'ANSWER_B_Q2',
                'instruction': '[QUESTION 2+] Click on answer option B (after screen shift) and press SPACE'
            },
            {
                'name': 'ANSWER_C_Q2',
                'instruction': '[QUESTION 2+] Click on answer option C (after screen shift) and press SPACE'
            },
            {
                'name': 'ANSWER_D_Q2',
                'instruction': '[QUESTION 2+] Click on answer option D (after screen shift) and press SPACE'
            },
            {
                'name': 'NEXT_BUTTON_Q2',
                'instruction': '[QUESTION 2+] Move mouse to NEXT button (after screen shift) and press SPACE'
            },
            # Gemini coordinates
            {
                'name': 'GEMINI_INPUT_FIELD',
                'instruction': 'Move mouse to Gemini input field and press SPACE'
            },
            {
                'name': 'GEMINI_SEND_BUTTON',
                'instruction': 'Move mouse to Gemini send button and press SPACE'
            },
            {
                'name': 'GEMINI_RESPONSE_TOP_LEFT',
                'instruction': 'Move mouse to TOP-LEFT of Gemini response area and press SPACE'
            },
            {
                'name': 'GEMINI_RESPONSE_BOTTOM_RIGHT',
                'instruction': 'Move mouse to BOTTOM-RIGHT of Gemini response area and press SPACE'
            },
        ]
        
    def on_press(self, key):
        """Handle keyboard press events"""
        try:
            # Space key to capture coordinate
            if key == Key.space:
                pos = pyautogui.position()
                step_name = self.steps[self.current_step]['name']
                self.coordinates[step_name] = {'x': pos[0], 'y': pos[1]}
                
                print(f"✓ Captured: {step_name} at ({pos[0]}, {pos[1]})")
                
                self.current_step += 1
                
                if self.current_step >= len(self.steps):
                    print("\n" + "="*60)
                    print("Calibration complete! Generating config.py...")
                    print("="*60)
                    self.save_config()
                    self.running = False
                    return False
                else:
                    print(f"\nStep {self.current_step + 1}/{len(self.steps)}:")
                    print(self.steps[self.current_step]['instruction'])
                    
            # ESC to quit
            elif key == Key.esc:
                print("\nCalibration cancelled.")
                self.running = False
                return False
                
        except AttributeError:
            pass
    
    def save_config(self):
        """Generate config.py with captured coordinates"""
        
        # Calculate areas from corner coordinates
        quiz_area = {
            'x': self.coordinates['QUIZ_QUESTION_AREA_TOP_LEFT']['x'],
            'y': self.coordinates['QUIZ_QUESTION_AREA_TOP_LEFT']['y'],
            'width': self.coordinates['QUIZ_QUESTION_AREA_BOTTOM_RIGHT']['x'] - 
                     self.coordinates['QUIZ_QUESTION_AREA_TOP_LEFT']['x'],
            'height': self.coordinates['QUIZ_QUESTION_AREA_BOTTOM_RIGHT']['y'] - 
                      self.coordinates['QUIZ_QUESTION_AREA_TOP_LEFT']['y']
        }
        
        gemini_area = {
            'x': self.coordinates['GEMINI_RESPONSE_TOP_LEFT']['x'],
            'y': self.coordinates['GEMINI_RESPONSE_TOP_LEFT']['y'],
            'width': self.coordinates['GEMINI_RESPONSE_BOTTOM_RIGHT']['x'] - 
                     self.coordinates['GEMINI_RESPONSE_TOP_LEFT']['x'],
            'height': self.coordinates['GEMINI_RESPONSE_BOTTOM_RIGHT']['y'] - 
                      self.coordinates['GEMINI_RESPONSE_TOP_LEFT']['y']
        }
        
        config_content = f'''"""
Configuration file for MCQ Quiz Automation
Auto-generated by calibration.py
"""

# ============================================================================
# SCREEN COORDINATES - Auto-calibrated
# ============================================================================

# Quiz Screen Coordinates
QUIZ_QUESTION_AREA = {{
    'x': {quiz_area['x']},
    'y': {quiz_area['y']},
    'width': {quiz_area['width']},
    'height': {quiz_area['height']}
}}

# Individual answer option buttons - QUESTION 1
ANSWER_OPTIONS_Q1 = {{
    'A': {{'x': {self.coordinates['ANSWER_A_Q1']['x']}, 'y': {self.coordinates['ANSWER_A_Q1']['y']}}},
    'B': {{'x': {self.coordinates['ANSWER_B_Q1']['x']}, 'y': {self.coordinates['ANSWER_B_Q1']['y']}}},
    'C': {{'x': {self.coordinates['ANSWER_C_Q1']['x']}, 'y': {self.coordinates['ANSWER_C_Q1']['y']}}},
    'D': {{'x': {self.coordinates['ANSWER_D_Q1']['x']}, 'y': {self.coordinates['ANSWER_D_Q1']['y']}}},
}}

# Individual answer option buttons - QUESTION 2+ (after screen shift)
ANSWER_OPTIONS_Q2 = {{
    'A': {{'x': {self.coordinates['ANSWER_A_Q2']['x']}, 'y': {self.coordinates['ANSWER_A_Q2']['y']}}},
    'B': {{'x': {self.coordinates['ANSWER_B_Q2']['x']}, 'y': {self.coordinates['ANSWER_B_Q2']['y']}}},
    'C': {{'x': {self.coordinates['ANSWER_C_Q2']['x']}, 'y': {self.coordinates['ANSWER_C_Q2']['y']}}},
    'D': {{'x': {self.coordinates['ANSWER_D_Q2']['x']}, 'y': {self.coordinates['ANSWER_D_Q2']['y']}}},
}}

# Next question button - QUESTION 1
NEXT_BUTTON_Q1 = {{'x': {self.coordinates['NEXT_BUTTON_Q1']['x']}, 'y': {self.coordinates['NEXT_BUTTON_Q1']['y']}}}

# Next question button - QUESTION 2+ (after screen shift)
NEXT_BUTTON_Q2 = {{'x': {self.coordinates['NEXT_BUTTON_Q2']['x']}, 'y': {self.coordinates['NEXT_BUTTON_Q2']['y']}}}

# Gemini Screen Coordinates
GEMINI_INPUT_FIELD = {{'x': {self.coordinates['GEMINI_INPUT_FIELD']['x']}, 'y': {self.coordinates['GEMINI_INPUT_FIELD']['y']}}}
GEMINI_SEND_BUTTON = {{'x': {self.coordinates['GEMINI_SEND_BUTTON']['x']}, 'y': {self.coordinates['GEMINI_SEND_BUTTON']['y']}}}
GEMINI_RESPONSE_AREA = {{
    'x': {gemini_area['x']},
    'y': {gemini_area['y']},
    'width': {gemini_area['width']},
    'height': {gemini_area['height']}
}}

# ============================================================================
# TIMING SETTINGS - Adjust based on your system speed and internet
# ============================================================================

DELAY_AFTER_CLICK = 0.5
DELAY_AFTER_PASTE = 0.3
DELAY_FOR_GEMINI_RESPONSE = 3.0
DELAY_BETWEEN_QUESTIONS = 1.0

PYAUTOGUI_PAUSE = 0.25
PYAUTOGUI_FAILSAFE = True

# ============================================================================
# AUTOMATION BEHAVIOR
# ============================================================================

QUESTION_SELECTION_METHOD = 'triple_click'
COPY_METHOD = 'ctrl_c'
USE_OCR = False
EXPECTED_ANSWER_FORMAT = 'letter'

# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

EMERGENCY_STOP_KEY = 'esc'
START_KEY = 'f9'

# ============================================================================
# LOGGING AND DEBUG
# ============================================================================

DEBUG_MODE = True
SAVE_SCREENSHOTS = True
SCREENSHOT_DIR = 'debug_screenshots'
LOG_FILE = 'quiz_automation.log'
'''
        
        with open('config.py', 'w') as f:
            f.write(config_content)
        
        print("\n✓ config.py has been updated with your calibrated coordinates!")
        print("\nYou can now run main.py to start the automation.")
    
    def run(self):
        """Start the calibration process"""
        print("="*60)
        print("MCQ Quiz Automation - Calibration Tool")
        print("="*60)
        print("\nInstructions:")
        print("- Move your mouse to each requested position")
        print("- Press SPACE to capture the coordinate")
        print("- Press ESC to cancel at any time")
        print("\nMake sure both your quiz and Gemini are visible on screen!")
        print("\nStarting in 3 seconds...")
        print("="*60)
        
        time.sleep(3)
        
        print(f"\nStep 1/{len(self.steps)}:")
        print(self.steps[0]['instruction'])
        
        # Start listening for keyboard events
        with kb.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    try:
        calibrator = CalibrationTool()
        calibrator.run()
    except KeyboardInterrupt:
        print("\n\nCalibration cancelled by user.")
        sys.exit(0)
