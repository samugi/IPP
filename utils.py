#import win32gui
#import win32con
#import win32api
import random
import pyautogui
import subprocess
import time
import keyboard
import datetime
from time import sleep
from Comment import Comment
#from PIL import ImageGrab

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

def stampWindowPath(path,name):
	pyautogui.hotkey('alt', 'print screen')
	sleep(.500)
	#img = ImageGrab.grabclipboard()
	#img.save(path+name, 'JPEG')
	
def sendCommand(command):
	command = convertCommandInEnum(command)
	if command == 1:	
		#press A
		pyautogui.keyDown('a')
		time.sleep(.250)
		pyautogui.keyUp('a')
		print("Button pressed: A")
	elif command == 2:
		#press Z
		pyautogui.keyDown('z')
		time.sleep(.250)
		pyautogui.keyUp('z')
		print("Button pressed: B")
	elif command == 3:
		#press I (UP)
		pyautogui.keyDown('i')
		time.sleep(.250)
		pyautogui.keyUp('i')
		print("Button pressed: Arrow UP")
	elif command == 4:
		#press K (DOWN)
		pyautogui.keyDown('k')
		time.sleep(.250)
		pyautogui.keyUp('k')
		print("Button pressed: Arrow DOWN")
	elif command == 5:
		#press J (LEFT)
		pyautogui.keyDown('j')
		time.sleep(.250)
		pyautogui.keyUp('j')
		print("Button pressed: Arrow LEFT")
	elif command == 6:
		#press L (RIGHT)
		pyautogui.keyDown('l')
		time.sleep(.250)
		pyautogui.keyUp('l')
		print("Button pressed: Arrow RIGHT")
	elif command == 7:
		#press P (start)
		pyautogui.keyDown('p')
		time.sleep(.250)
		pyautogui.keyUp('p')
		print("Button pressed: START")

def stampWindow():
	keyboard.press_and_release("alt+print screen")		

def sendCommands(command, n):
	for x in range(0, int(n)):
		sendCommand(command)

def execWithOutput(command):
	return subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0].decode("utf-8") 

def fillCommentsList(nextCommentIndex, commentsJArr):
	commentsList = []
	for i in range (nextCommentIndex, -1, -1):
		c = Comment(commentsJArr[i]["id"], commentsJArr[i]["text"])
		c.username = commentsJArr[i]["username"]
		c.likeCount = commentsJArr[i]["like_count"]
		c.repliesCount = len(commentsJArr[i]["replies"]["data"]) if "replies" in commentsJArr[i] else 0
		c.timestamp = commentsJArr[i]["timestamp"]
		commentsList.append(c)
	return commentsList