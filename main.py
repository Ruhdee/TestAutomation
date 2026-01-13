"""
Main Script for MCQ Quiz Automation
Run this after calibration to start the automation

Usage:
1. Open your quiz in one half of the screen
2. Open Gemini chat in the other half
3. Set up Gemini with system instructions (see README.md)
4. Run this script
5. Press F9 to start automation
6. Press ESC to stop at any time
"""

import time
import sys
import keyboard
from quiz_automation import QuizAutomation
import config


def print_banner():
    """Print welcome banner"""
    print("="*70)
    print(" "*20 + "MCQ Quiz Automation")
    print("="*70)
    print()


def print_instructions():
    """Print usage instructions"""
    print("Setup Checklist:")
    print("  ✓ Quiz is open on one side of screen")
    print("  ✓ Gemini chat is open on other side")
    print("  ✓ Gemini has system instructions configured")
    print("  ✓ You've run calibration.py to set coordinates")
    print()
    print("Controls:")
    print(f"  • Press {config.START_KEY.upper()} to START automation")
    print(f"  • Press {config.EMERGENCY_STOP_KEY.upper()} to STOP at any time")
    print()
    print("="*70)
    print()


def setup_gemini_instructions():
    """Display recommended Gemini system instructions"""
    print("System Instructions:\n")
    print("""
You are helping with an MCQ quiz. When given a screenshot of a question 
with multiple choice options, analyze the image and respond with ONLY 
the letter of the correct answer (A, B, C, or D).

CONTEXT - Algorand Blockchain:
- Algorand is a blockchain platform using Pure Proof-of-Stake (PPoS) consensus
- Key features: 10,000+ TPS, instant finality, low fees, carbon-negative
- Supports smart contracts and dApps
- Native token: ALGO
- Uses Verifiable Random Function (VRF) for validator selection

IMPORTANT RULES:
1. Respond with ONLY a single letter: A, B, C, or D
2. Do NOT provide explanations or analysis
3. Do NOT append to previous answers
4. Each response should be ONLY the current answer, nothing else
5. Forget all previous questions - only answer the current one

Example:
[Image shows: What is 2+2? A) 3 B) 4 C) 5 D) 6]
Your response: B

[Next image shows: What is 3+3? A) 5 B) 6 C) 7 D) 8]
Your response: B
(NOT "B B" or "Previous: B, Current: B")
    """)
    print("-" * 70)
    print()


def wait_for_start():
    """Wait for user to press start key"""
    print(f"Press {config.START_KEY.upper()} when ready to start...")
    keyboard.wait(config.START_KEY)
    print("\nStarting automation in 3 seconds...")
    print("Position your windows now!")
    time.sleep(3)
    print("\n🚀 AUTOMATION STARTED!\n")


def main():
    """Main function"""
    print_banner()
    print_instructions()
    setup_gemini_instructions()
    
    # Ask user if they want to see instructions
    response = input("Have you set up Gemini with system instructions? (y/n): ")
    if response.lower() != 'y':
        print("\nPlease set up Gemini first with the instructions shown above.")
        print("You can paste them into Gemini's system instructions.")
        return
    
    print()
    
    # Ask how many questions to process
    try:
        num_questions = input("How many questions to process? (Enter for unlimited): ")
        if num_questions.strip():
            num_questions = int(num_questions)
        else:
            num_questions = float('inf')
    except ValueError:
        print("Invalid number, defaulting to unlimited")
        num_questions = float('inf')
    
    print()
    
    # Wait for start signal
    wait_for_start()
    
    # Create automation instance
    automation = QuizAutomation()
    
    # Setup emergency stop
    stop_flag = {'stop': False}
    
    def emergency_stop():
        """Emergency stop handler"""
        stop_flag['stop'] = True
        print("\n\n⚠️  EMERGENCY STOP ACTIVATED!")
        print("Automation stopped safely.")
    
    keyboard.add_hotkey(config.EMERGENCY_STOP_KEY, emergency_stop)
    
    # Main automation loop
    questions_processed = 0
    
    try:
        while questions_processed < num_questions and not stop_flag['stop']:
            success = automation.process_question()
            
            if not success:
                print("\n❌ Error occurred. Stopping automation.")
                break
            
            questions_processed += 1
            
            if questions_processed < num_questions:
                print(f"\n✓ Progress: {questions_processed} questions completed")
                print(f"  Next question in {config.DELAY_BETWEEN_QUESTIONS}s...")
        
        if not stop_flag['stop']:
            print("\n" + "="*70)
            print(f"🎉 AUTOMATION COMPLETE!")
            print(f"   Processed {questions_processed} questions")
            print("="*70)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        automation.log(f"FATAL ERROR: {str(e)}")
    
    finally:
        # Cleanup
        keyboard.unhook_all()
        print("\nAutomation ended.")
        print(f"Check {config.LOG_FILE} for detailed logs.")
        if config.SAVE_SCREENSHOTS:
            print(f"Screenshots saved in {config.SCREENSHOT_DIR}/")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)
