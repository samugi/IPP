import win32gui
import win32con
import win32api
import random
import keyboard
import time
from time import sleep
from Comment import Comment
from PIL import ImageGrab

def is_win_ok(hwnd, starttext):
    s = win32gui.GetWindowText(hwnd)
    if s.startswith(starttext):
            print(s)
            global MAIN_HWND
            MAIN_HWND = hwnd
            return None
    return 1


def find_main_window(starttxt):
    global MAIN_HWND
    win32gui.EnumChildWindows(0, is_win_ok, starttxt)
    return MAIN_HWND


def winfun(hwnd, lparam):
    s = win32gui.GetWindowText(hwnd)
    if len(s) > 3:
        print("winfun, child_hwnd: %d   txt: %s" % (hwnd, s))
    return 1

def main():
    main_app = 'VisualBoyAdvance-'
    hwnd = win32gui.FindWindow(None, main_app)
    print("STEP 1")
    print(hwnd)
    if hwnd < 1:
        print("STEP 2")
        hwnd = find_main_window(main_app)
        win32gui.EnumChildWindows(hwnd, winfun, None)
    print("STEP 3")
    print(hwnd)
    return hwnd
	
def convertCommandInEnum(command):
	if "up" in command:
		return 3
	elif "su" in command:
		return 3
	elif "avanti" in command:
		return 3
	elif "down" in command:
		return 4
	elif "giù" in command:
		return 4
	elif "giu" in command:
		return 4
	elif "a" in command:
		return 1
	elif "ok" in command:
		return 1
	elif "b" in command:
		return 2
	elif "no" in command:
		return 2
	elif "left" in command:
		return 5
	elif "sinistra" in command:
		return 5
	elif "sx" in command:
		return 5
	elif "lf" in command:
		return 5
	elif "right" in command:
		return 6 
	elif "destra" in command:
		return 6 
	elif "dx" in command:
		return 6
	elif "rt" in command:
		return 6
	elif "start" in command:
		return 7
	elif "menu" in command:
		return 7
	elif "pause" in command:
		return 7
	elif "pausa" in command:
		return 7
	elif "p" in command:
		return 7

def stampWindow(path,name)
	keyboard.press_and_release("alt+print screen")
	sleep(.500)
	img = ImageGrab.grabclipboard()
	img.save(path+name, 'JPEG')
	
def sendCommand(command):
	command = convertCommandInEnum(command)
	if command == 1:	
		#press A
		keyboard.press('a')
		time.sleep(.250)
		keyboard.release('a')
		print("Button pressed: A")
	elif command == 2:
		#press Z
		keyboard.press('z')
		time.sleep(.250)
		keyboard.release('z')
		print("Button pressed: B")
	elif command == 3:
		#press I (UP)
		keyboard.press('i')
		time.sleep(.250)
		keyboard.release('i')
		print("Button pressed: Arrow UP")
	elif command == 4:
		#press K (DOWN)
		keyboard.press('k')
		time.sleep(.250)
		keyboard.release('k')
		print("Button pressed: Arrow DOWN")
	elif command == 5:
		#press J (LEFT)
		keyboard.press('j')
		time.sleep(.250)
		keyboard.release('j')
		print("Button pressed: Arrow LEFT")
	elif command == 6:
		#press L (RIGHT)
		keyboard.press('l')
		time.sleep(.250)
		keyboard.release('l')
		print("Button pressed: Arrow RIGHT")
	elif command == 7:
		#press P (start)
		keyboard.press('p')
		time.sleep(.250)
		keyboard.release('p')
		print("Button pressed: START")
		
def sendCommands(command, n):
	for x in range(1, int(n)):
		sendCommand(command)
