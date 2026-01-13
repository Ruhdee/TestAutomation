# MCQ Quiz Automation

Automate online MCQ quizzes using PyAutoGUI and Gemini AI in split-screen mode.

## Features

✨ **Easy to Configure** - All settings in one `config.py` file  
🎯 **Interactive Calibration** - Visual tool to capture screen coordinates  
🔧 **Modular Design** - Each function is independent and easy to modify  
⚡ **Safe Controls** - Emergency stop and pause functionality  
📝 **Detailed Logging** - Track every action with screenshots  

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The script now uses **screenshot mode** to capture questions as images and paste them into Gemini, which works even when text copying is disabled on the quiz platform.

### 2. Run Calibration

```bash
python calibration.py
```

Follow the on-screen instructions to capture coordinates for:
- Quiz question area
- Answer options (A, B, C, D)
- Next button
- Gemini input field and response area

### 3. Set Up Gemini

Open Gemini chat and configure with these system instructions:

```
You are helping with an MCQ quiz. When given a question with multiple choice
options, respond with ONLY the letter of the correct answer (A, B, C, or D).

Do not provide explanations, just the single letter.

Example:
Question: What is 2+2? A) 3 B) 4 C) 5 D) 6
Your response: B
```

### 4. Run Automation

```bash
python main.py
```

**Setup your screen:**
- Quiz on one side (left or right half)
- Gemini chat on the other side
- Press **F9** to start
- Press **ESC** to stop anytime

## Configuration

All settings are in `config.py`. You can easily modify:

### Screen Coordinates
```python
QUIZ_QUESTION_AREA = {'x': 100, 'y': 200, 'width': 600, 'height': 400}
ANSWER_OPTIONS = {
    'A': {'x': 150, 'y': 450},
    'B': {'x': 150, 'y': 500},
    # ...
}
```

### Timing Settings
```python
DELAY_AFTER_CLICK = 0.5          # Adjust for slower systems
DELAY_FOR_IMAGE_UPLOAD = 2.0     # Wait for image upload before sending
DELAY_FOR_GEMINI_RESPONSE = 3.0  # Increase if Gemini is slow
DELAY_BETWEEN_QUESTIONS = 1.0    # Pause between questions
```

### Behavior Settings
```python
QUESTION_SELECTION_METHOD = 'triple_click'  # or 'ctrl_a', 'drag'
COPY_METHOD = 'ctrl_c'                      # or 'right_click_menu'
EXPECTED_ANSWER_FORMAT = 'letter'           # or 'number'
```

## How It Works

1. **Capture Question Screenshot**: Takes a screenshot of the question area (works even when copying is disabled)
2. **Paste to Gemini**: Pastes the screenshot image into Gemini chat
3. **Wait for Response**: Automatically detects when Gemini finishes processing
4. **Parse Answer**: Extracts the correct option (A, B, C, or D) from Gemini's text response
5. **Select Answer**: Clicks the correct option on quiz screen
6. **Next Question**: Clicks next button and repeats

## Customization Guide

### Changing Selection Method

In `config.py`:
```python
# Triple-click (best for paragraph text)
QUESTION_SELECTION_METHOD = 'triple_click'

# Ctrl+A (best for text boxes)
QUESTION_SELECTION_METHOD = 'ctrl_a'

# Drag selection (best for specific areas)
QUESTION_SELECTION_METHOD = 'drag'
```

### Adjusting for Different Quiz Layouts

1. Run `calibration.py` again to recapture coordinates
2. Or manually edit coordinates in `config.py`
3. Test with a single question first

### Modifying Answer Parsing

Edit the `parse_answer()` function in `quiz_automation.py`:

```python
def parse_answer(self, response):
    # Add your custom parsing logic here
    # Example: handle "Option A" format
    if "Option" in response:
        match = re.search(r'Option ([A-D])', response)
        if match:
            return match.group(1)
    # ... rest of parsing
```

### Adding More Answer Options

In `config.py`, add more options:
```python
ANSWER_OPTIONS = {
    'A': {'x': 150, 'y': 450},
    'B': {'x': 150, 'y': 500},
    'C': {'x': 150, 'y': 550},
    'D': {'x': 150, 'y': 600},
    'E': {'x': 150, 'y': 650},  # Add option E
}
```

## Troubleshooting

### Question not copying correctly
- Try different `QUESTION_SELECTION_METHOD` in config
- Increase `DELAY_AFTER_CLICK`
- Check if question area coordinates are accurate

### Gemini response not captured
- Increase `DELAY_FOR_GEMINI_RESPONSE`
- Verify Gemini response area coordinates
- Check if Gemini is responding in expected format

### Wrong answer selected
- Verify answer option coordinates in calibration
- Check Gemini's system instructions
- Review `parse_answer()` logic in `quiz_automation.py`

### Automation too fast/slow
- Adjust timing delays in `config.py`
- Modify `PYAUTOGUI_PAUSE` for global speed control

## Debug Mode

Enable detailed logging in `config.py`:
```python
DEBUG_MODE = True
SAVE_SCREENSHOTS = True
```

This will:
- Save detailed logs to `quiz_automation.log`
- Capture screenshots at each step in `debug_screenshots/`

## File Structure

```
TestAutomation/
├── main.py              # Main script to run
├── quiz_automation.py   # Core automation logic
├── config.py            # All configuration settings
├── calibration.py       # Interactive calibration tool
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── quiz_automation.log # Log file (generated)
└── debug_screenshots/  # Screenshots (generated)
```

## Safety Features

- **Emergency Stop**: Press ESC anytime to stop
- **Failsafe**: Move mouse to screen corner to abort
- **Error Handling**: Continues on minor errors, stops on critical ones
- **Logging**: All actions logged for review

## Tips for Best Results

1. **Use a stable internet connection** - Gemini needs to respond quickly
2. **Keep windows in fixed positions** - Don't move them during automation
3. **Test with 1-2 questions first** - Verify everything works before full run
4. **Adjust delays** - Slower systems may need longer delays
5. **Monitor first few questions** - Ensure accuracy before leaving unattended

## License

Free to use and modify for educational purposes.

## Disclaimer

This tool is for educational purposes. Ensure you have permission to automate quiz-taking on your platform. Use responsibly and ethically.
