# DuckyScript → pyautogui Translator

Minimal Python function that converts **DuckyScript 3.x** payloads into executable **pyautogui** code.

## What it does
- Supports `DEFAULT_DELAY`, `DELAY`, `STRING`, `STRINGLN`, `REPEAT`
- Handles key combos like `GUI r`, `CTRL ALT DEL`
- Outputs Python code or executes it directly

## Requirements
- Python 3.x
- `pyautogui`

```bash
pip install pyautogui
```

## Usage
```python
from toducky import toducky

code = toducky(payload, execute=False)
toducky(payload, execute=True)
```

## Notes
- This is **not** real HID emulation
- Timing and layout depend on the OS and pyautogui
