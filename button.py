import pyautogui

# Take a screenshot of the upload button on your screen and save it to "upload_button.png"
# (Make sure the upload button is visible on your screen before running this)
# Example: pyautogui.screenshot(region=(x, y, width, height)).save('upload_button.png')

# Find the position of the upload button image within the screen
upload_button_position = pyautogui.locateCenterOnScreen('"C:\\Users\\santo\\Pictures\\Screenshots\\button.png"')

if upload_button_position is not None:
    print("Upload button found at:", upload_button_position)
else:
    print("Upload button not found.")
