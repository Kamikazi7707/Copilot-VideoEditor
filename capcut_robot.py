import pyautogui
import time
import pygetwindow as gw

def focus_capcut():
    # Brings CapCut window to the front (Windows/Mac)
    windows = gw.getWindowsWithTitle('CapCut')
    if windows:
        windows[0].activate()
        time.sleep(0.2)
    else:
        print("CapCut window not found.")

def split_clip():
    focus_capcut()
    pyautogui.hotkey('ctrl', 'b')  # Default split shortcut

# Usage:
if __name__ == '__main__':
    print("Switch to CapCut. Splitting in 3 seconds...")
    time.sleep(3)
    split_clip()
