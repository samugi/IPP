#you will need the win32 libraries for this snippet of code to work, Links below
import win32gui
import win32con
import win32api
import random
import keyboard
import time
from time import sleep
from Comment import Comment

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

def sendCommand(command):
	command = convertCommandInEnum(command)
	if command == 1:	
		#press A
		keyboard.press('a')
		sleep(.250)
		keyboard.release('a')
		print("Button pressed: A")
	elif command == 2:
		#press Z
		keyboard.press('z')
		sleep(.250)
		keyboard.release('z')
		print("Button pressed: B")
	elif command == 3:
		#press I (UP)
		keyboard.press('i')
		sleep(.250)
		keyboard.release('i')
		print("Button pressed: Arrow UP")
	elif command == 4:
		#press K (DOWN)
		keyboard.press('k')
		sleep(.250)
		keyboard.release('k')
		print("Button pressed: Arrow DOWN")
	elif command == 5:
		#press J (LEFT)
		keyboard.press('j')
		sleep(.250)
		keyboard.release('j')
		print("Button pressed: Arrow LEFT")
	elif command == 6:
		#press L (RIGHT)
		keyboard.press('l')
		sleep(.250)
		keyboard.release('l')
		print("Button pressed: Arrow RIGHT")
	elif command == 7:
		#press P (start)
		keyboard.press('p')
		sleep(.250)
		keyboard.release('p')
		print("Button pressed: START")
		
def sendCommands(command, n):
	for x in range(1, n):
		sendCommand(command)
#[hwnd] No matter what people tell you, this is the handle meaning unique ID, 
#["Notepad"] This is the application main/parent name, an easy way to check for examples is in Task Manager
#["test - Notepad"] This is the application sub/child name, an easy way to check for examples is in Task Manager clicking dropdown arrow
#hwndMain = win32gui.FindWindow("Notepad", "test - Notepad") this returns the main/parent Unique ID
hwndMain = main()#win32gui.FindWindow("Notepad", "Untitled - Notepad")
print(hwndMain) #you can use this to see main/parent Unique ID
#["hwndMain"] this is the main/parent Unique ID used to get the sub/child Unique ID
#[win32con.GW_CHILD] I havent tested it full, but this DOES get a sub/child Unique ID, if there are multiple you'd have too loop through it, or look for other documention, or i may edit this at some point ;)
#hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD) this returns the sub/child Unique ID
hwndChild =  hwndMain #win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
win32gui.SetForegroundWindow(hwndChild)
print(hwndChild)  #you can use this to see sub/child Unique ID

#While(True) Will always run and continue to run indefinitely
while(True):
	#[hwndChild] this is the Unique ID of the sub/child application/proccess
	#[win32con.WM_CHAR] This sets what PostMessage Expects for input theres KeyDown and KeyUp as well
	#[0x44] hex code for D
	#[0]No clue, good luck!
	#temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0) returns key sent
	
	commentsArray = ["up", "down", "avanti", "destra", "ok", "no"]
	
	for comment in commentsArray:
		words = comment["text"].split(" ")
		print(words[0])
		if len(words) > 2:
			print("More then one words")
			continue
		elif len(words) == 2:
			print("Two words")
			if words[0].isnumeric():
				if words[0] <= 10:
					sendCommands(words[1],words[0])
				continue
			continue
		elif len(words) == 1:
			print("One word")
			sendCommand(words[0])
	#print(temp) prints the returned value of temp, into the console
	#sleep(1) this waits 1 second before looping through again
	sleep(1)
