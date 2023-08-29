import subprocess
import osascript
import pyautogui
import time

def auto_post(caption):
    # 1. OPEN SAFARI
    subprocess.call(['open', '-a', 'Safari'])
    # 2. NAVIGATE TO INSTAGRAM.COM
    url = 'https://www.instagram.com'
    osascript.osascript('tell application "Safari" to open location "{0}"'.format(url))
    # 3. CLICK CREATE POST
    time.sleep(4)
    create_button = pyautogui.locateOnScreen('pyautogui_images/create_ig_post.png')
    pyautogui.click(create_button)
    time.sleep(2)
    # 4. UPLOAD IMAGE
    add_photo = pyautogui.locateOnScreen('pyautogui_images/add_photo.png')
    pyautogui.click(add_photo)
    time.sleep(2)
    ig_photo = pyautogui.locateOnScreen('pyautogui_images/ig_photo.png')
    pyautogui.click(ig_photo)
    time.sleep(1)
    upload_photo = pyautogui.locateOnScreen('pyautogui_images/upload_photo.png')
    pyautogui.click(upload_photo)
    time.sleep(5)
    next_button = pyautogui.locateOnScreen('pyautogui_images/next_button.png')
    pyautogui.click(next_button)
    pyautogui.move(0, -50)
    time.sleep(3)
    next_button2 = pyautogui.locateOnScreen('pyautogui_images/next_button2.png')
    pyautogui.click(next_button2)
    time.sleep(3)
    # 5. PASTE CAPTION 
    caption_space = pyautogui.locateOnScreen('pyautogui_images/caption_space.png')
    pyautogui.click(caption_space)
    time.sleep(1.5)
    pyautogui.write(caption)
    time.sleep(2)
    # 6. POST
    share_button = pyautogui.locateOnScreen('pyautogui_images/share_button.png')
    pyautogui.click(share_button)

if __name__ =='__main__':
    auto_post('AI is lit AF.')
