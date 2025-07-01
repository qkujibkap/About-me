import pyautogui
import datetime
import os
import keyboard  # для горячих клавиш
import threading

def take_screenshot(save_dir="screenshots"):
    os.makedirs(save_dir, exist_ok=True)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    filepath = os.path.join(save_dir, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"[+] Скриншот сохранен: {filepath}")

def listen_hotkey():
    print("Ожидание горячей клавиши Ctrl+Shift+S для скриншота...")
    keyboard.add_hotkey("ctrl+shift+s", take_screenshot)
    keyboard.wait()  # Блокирует поток, пока не нажмешь esc или ctrl+c

if __name__ == "__main__":
    thread = threading.Thread(target=listen_hotkey)
    thread.start()
    thread.join()