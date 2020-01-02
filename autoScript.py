#you will need the win32 libraries for this snippet of code to work, Links below
import win32gui
import win32con
import win32api
import random
import time
from time import sleep

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
	


#[hwnd] No matter what people tell you, this is the handle meaning unique ID, 
#["Notepad"] This is the application main/parent name, an easy way to check for examples is in Task Manager
#["test - Notepad"] This is the application sub/child name, an easy way to check for examples is in Task Manager clicking dropdown arrow
#hwndMain = win32gui.FindWindow("Notepad", "test - Notepad") this returns the main/parent Unique ID
hwndMain = main() #win32gui.FindWindow("VisualBoyAdvance emulator (32 bit)", "VisualBoyAdvance")
print(hwndMain) #you can use this to see main/parent Unique ID
#["hwndMain"] this is the main/parent Unique ID used to get the sub/child Unique ID
#[win32con.GW_CHILD] I havent tested it full, but this DOES get a sub/child Unique ID, if there are multiple you'd have too loop through it, or look for other documention, or i may edit this at some point ;)
#hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD) this returns the sub/child Unique ID
hwndChild = hwndMain
print(hwndChild)  #you can use this to see sub/child Unique ID

#While(True) Will always run and continue to run indefinitely
while(True):
	#[hwndChild] this is the Unique ID of the sub/child application/proccess
	#[win32con.WM_CHAR] This sets what PostMessage Expects for input theres KeyDown and KeyUp as well
	#[0x44] hex code for D
	#[0]No clue, good luck!
	#temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0) returns key sent
	r = random.randint(1,7)
	
	if r == 1:	
		#press A
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x41, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x41, 0)
		print("Ho premuto A")
	elif r == 2:
		#press Z
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x5A, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x5A, 0)
		print("Ho premuto Z")
	elif r == 3:
		#press I (UP)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x49, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x49, 0)
		print("Ho premuto I")
	elif r == 4:
		#press K (DOWN)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x4B, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x4B, 0)
		print("Ho premuto K")
	elif r == 5:
		#press J (LEFT)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x4A, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x4A, 0)
		print("Ho premuto J")
	elif r == 6:
		#press L (RIGHT)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x4C, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x4C, 0)
		print("Ho premuto L")
	elif r == 7:	
		#press P (start)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, 0x50, 0)
		time.sleep(1)
		temp = win32api.PostMessage(hwndChild, win32con.WM_KEYUP, 0x50, 0)
		print("Ho premuto P")


	#print(temp) prints the returned value of temp, into the console
	print(temp)
	#sleep(1) this waits 1 second before looping through again
	sleep(1)
