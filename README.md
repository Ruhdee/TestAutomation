# MCQ Quiz Automation

Automate online MCQ quizzes using browser automation and Gemini AI. The script captures question screenshots, sends them to Gemini, and automatically selects answers.

## ✨ Features

- 🎯 **Smart Screen Shift Detection** - Automatically adapts to UI changes between questions
- 📸 **Screenshot-Based** - Works even when text copying is disabled
- 🔄 **Reference Image Matching** - Reliable send button detection using visual comparison
- 📁 **Organized Debug Output** - Screenshots categorized by type (questions, responses, answers, etc.)
- ⚡ **Safe Controls** - Emergency stop (ESC) and manual override options
- 📝 **Detailed Logging** - Track every action with timestamps
- 🎨 **Dual Coordinate System** - Handles screen shifts automatically or manually

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `pyautogui` - Screen automation
- `Pillow` - Image processing
- `pyperclip` - Clipboard operations
- `keyboard` - Keyboard shortcuts
- `pynput` - Mouse/keyboard events (calibration)
- `pywin32` - Windows clipboard API
- `numpy` - Image similarity calculations

### 2. Run Calibration

```bash
python calibration.py
```

**Calibration captures TWO sets of coordinates:**
- **Q1 coordinates** - For Question 1 (before any screen shift)
- **Q2+ coordinates** - For Questions 2+ (after screen shift, if it occurs)

Follow the on-screen instructions to capture:
1. Quiz question area
2. Answer options A, B, C, D (for Q1)
3. Next button (for Q1)
4. Answer options A, B, C, D (for Q2+)
5. Next button (for Q2+)
6. Gemini input field
7. Gemini send button
8. Gemini response area

### 3. Capture Send Button References (Optional but Recommended)

```bash
python capture_send_button_refs.py
```

This creates reference images for reliable send button detection:
- **Ready state** - Send button after image upload completes
- **Sent state** - Blue stop square visible after sending

### 4. Set Up Gemini

Open Gemini chat and configure with these system instructions:

```
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
```

### 5. Run Automation

```bash
python main.py
```

**Setup your screen:**
- Quiz on one side (left or right half)
- Gemini chat on the other side
- Press **F9** to start
- Press **ESC** to stop anytime

## 🎯 How It Works

### Main Workflow

1. **Capture Screenshot** - Takes screenshot of question area
2. **Paste to Gemini** - Pastes image into Gemini chat with system prompt
3. **Wait for Upload** - Monitors send button using reference image matching
4. **Click Send** - Verifies send by detecting blue stop square
5. **Get Response** - Polls response area for valid answer (A-D)
6. **Parse Answer** - Extracts last valid letter (handles appended answers)
7. **Select Answer** - Clicks correct option using appropriate coordinates
8. **Click Next** - Moves to next question
9. **Screen Shift Check** - After Q1, detects if UI shifted and adjusts coordinates

### Screen Shift Detection

The script automatically detects if the quiz UI shifts after the first question:

1. **Before selecting answer on Q1** - Captures 20x20px region (22, 454)
2. **After clicking Next on Q1** - Captures same region again
3. **Compares images** - If similarity < 95%, screen shifted
4. **Switches coordinates** - Uses Q2+ coordinates for all remaining questions

**Manual Override Available:**
```python
# In config.py
USE_SCREEN_SHIFT_DETECTION = False  # Disable auto-detection
MANUAL_COORDINATE_SET = 'Q1'  # or 'Q2' - force specific coordinates
```

### Reference Image Matching

Instead of unreliable change detection, the script uses visual matching:

**Send Button Ready:**
- Compares current button with `reference_images/send_button_ready.png`
- 85% similarity threshold
- Ensures upload completed before sending

**Message Sent:**
- Compares with `reference_images/send_button_sent.png` (blue stop square)
- 85% similarity threshold
- Confirms message was actually sent

**Fallback:** If reference images missing, uses stability-based detection

## 📁 Debug Screenshots

All screenshots are organized into categorized folders:

```
debug_screenshots/
├── questions/          # Question captures & after-next screenshots
├── gemini_input/       # Full screen after sending to Gemini
├── gemini_response/    # Response area captures
├── answers/            # Screenshots after selecting answers
├── screen_shift/       # Before/after shift comparison images
└── errors/             # Error screenshots
```

**Screen shift images saved:**
- `before_shift_q1.png` - Region before clicking Next on Q1
- `after_shift_q2.png` - Region after clicking Next (Q2 loaded)

## ⚙️ Configuration

### Screen Shift Detection

```python
# Enable/disable automatic screen shift detection
USE_SCREEN_SHIFT_DETECTION = True  # True = Auto-detect, False = Manual

# Manual coordinate selection (only used if USE_SCREEN_SHIFT_DETECTION = False)
MANUAL_COORDINATE_SET = 'Q1'  # Options: 'Q1' or 'Q2'
```

### Timing Settings

```python
DELAY_AFTER_CLICK = 0.5          # After clicking buttons
DELAY_AFTER_PASTE = 1            # After pasting image
DELAY_FOR_GEMINI_RESPONSE = 3.0  # Initial wait for response
DELAY_BETWEEN_QUESTIONS = 1.0    # Between questions
```

### Behavior Settings

```python
QUESTION_SELECTION_METHOD = 'triple_click'
COPY_METHOD = 'ctrl_c'
EXPECTED_ANSWER_FORMAT = 'letter'  # 'letter' or 'number'
```

### Debug Settings

```python
DEBUG_MODE = True
SAVE_SCREENSHOTS = True
SCREENSHOT_DIR = 'debug_screenshots'
LOG_FILE = 'quiz_automation.log'
```

## 🛠️ Utilities

### Mouse Tracker

```bash
python mouse_tracker.py
```

Displays real-time mouse coordinates - useful for manual calibration verification.

### Capture Send Button References

```bash
python capture_send_button_refs.py
```

Interactive tool to capture send button reference images:
1. Paste image into Gemini
2. Wait for upload to complete
3. Press SPACEBAR to capture "ready" state
4. Click send button
5. Wait for blue stop square
6. Press SPACEBAR to capture "sent" state

## 🔧 Troubleshooting

### Screen Shift Not Detected

**Symptoms:** Using wrong coordinates after Q1
**Solutions:**
- Check `debug_screenshots/screen_shift/` images
- Verify region (22, 454, 20x20) captures changing area
- Try manual mode: `USE_SCREEN_SHIFT_DETECTION = False`

### Send Button Not Clicking

**Symptoms:** Infinite retry loop on send button
**Solutions:**
- Run `capture_send_button_refs.py` to create reference images
- Check `reference_images/` folder exists with both PNG files
- Verify send button coordinates in calibration
- Check logs for similarity percentages

### Gemini Response Not Captured

**Symptoms:** "No valid response" warnings
**Solutions:**
- Increase `DELAY_FOR_GEMINI_RESPONSE`
- Verify response area coordinates
- Check Gemini is responding with single letter
- Review `debug_screenshots/gemini_response/` images

### Wrong Answer Selected

**Symptoms:** Clicking wrong option
**Solutions:**
- Verify answer coordinates in calibration
- Check if screen shifted (review logs)
- Try manual coordinate mode
- Review `debug_screenshots/answers/` images

### Gemini Appending Answers

**Symptoms:** Response like "D A B A"
**Solution:** Script automatically uses LAST letter, but ensure system instructions emphasize "forget previous questions"

## 📂 File Structure

```
TestAutomation/
├── main.py                      # Entry point
├── quiz_automation.py           # Core automation logic
├── config.py                    # Configuration (auto-generated by calibration)
├── calibration.py               # Dual-coordinate calibration tool
├── mouse_tracker.py             # Real-time mouse position display
├── capture_send_button_refs.py  # Send button reference capture
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── quiz_automation.log          # Log file (generated)
├── debug_screenshots/           # Organized screenshots (generated)
│   ├── questions/
│   ├── gemini_input/
│   ├── gemini_response/
│   ├── answers/
│   ├── screen_shift/
│   └── errors/
└── reference_images/            # Send button references (generated)
    ├── send_button_ready.png
    └── send_button_sent.png
```

## 🔒 Safety Features

- **Emergency Stop** - Press ESC anytime to stop
- **PyAutoGUI Failsafe** - Move mouse to screen corner to abort
- **Error Handling** - Continues on minor errors, stops on critical ones
- **Detailed Logging** - All actions logged with timestamps
- **Screenshot Evidence** - Every step captured for review
- **Manual Override** - Disable auto-detection if needed

## 💡 Tips for Best Results

1. **Run calibration carefully** - Accurate coordinates are crucial
2. **Create reference images** - Much more reliable than change detection
3. **Test with 1-2 questions first** - Verify everything works
4. **Monitor screen shift detection** - Check logs after Q1
5. **Review debug screenshots** - Identify issues quickly
6. **Adjust delays for your system** - Slower systems need longer delays
7. **Keep windows in fixed positions** - Don't move during automation
8. **Use stable internet** - Gemini needs consistent response times

## 🎓 Advanced Usage

### Custom Answer Parsing

Edit `parse_answer()` in `quiz_automation.py`:

```python
def parse_answer(self, response):
    # Uses LAST valid letter to handle appended answers
    matches = re.findall(r'\b([A-D])\b', response.upper())
    if matches:
        answer = matches[-1]  # Take the LAST match
        return answer
```

### Screen Shift Region Customization

In `quiz_automation.py`:

```python
self.screen_shift_region = (22, 454, 20, 20)  # x, y, width, height
```

Choose a region that:
- Changes when screen shifts
- Doesn't change when selecting answers
- Is consistent across questions

## 📝 License

Free to use and modify for educational purposes.

## ⚠️ Disclaimer

This tool is for educational purposes. Ensure you have permission to automate quiz-taking on your platform. Use responsibly and ethically.

## 🤝 Contributing

Contributions welcome! This is a learning project focused on browser automation and AI integration.

## 📧 Support

For issues or questions, check the debug screenshots and logs first. Most problems can be diagnosed by reviewing:
- `quiz_automation.log` - Detailed execution log
- `debug_screenshots/` - Visual evidence of each step
- `reference_images/` - Send button reference images
