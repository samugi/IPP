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
from PIL import ImageGrab


def initEventFile(FILE):
	global file
	file = FILE

def initController(A,B,U,D,L,R,S,SE):
	global a, b, up, down, left, right, start, select
	a = A
	b = B
	up = U
	down = D
	left = L
	right = R
	start = S
	select = SE

def getFile():
	return file


def convertCommandInLanguage(command):
	command = command.lower()
	if "up" in command:
		return "UP"
	elif "su" in command:
		return "UP"
	elif "avanti" in command:
		return "UP"
	elif "down" in command:
		return "DOWN"
	elif "giù" in command:
		return "DOWN"
	elif "giu" in command:
		return "DOWN"
	elif "a" in command:
		return "A"
	elif "ok" in command:
		return "A"
	elif "b" in command:
		return "B"
	elif "no" in command:
		return "B"
	elif "left" in command:
		return "LEFT"
	elif "sinistra" in command:
		return "LEFT"
	elif "sx" in command:
		return "LEFT"
	elif "lf" in command:
		return "LEFT"
	elif "right" in command:
		return "RIGHT"
	elif "destra" in command:
		return "RIGHT" 
	elif "dx" in command:
		return "RIGHT"
	elif "rt" in command:
		return "RIGHT"
	elif "start" in command:
		return "START"
	elif "menu" in command:
		return "START"
	elif "pause" in command:
		return "START"
	elif "pausa" in command:
		return "START"
	elif "p" in command:
		return "START"
	elif "select" in command:
		return "SELECT"

def convertCommandInEnum(command):
	command = command.lower()
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
	elif "select" in command:
		return 8

#FIXME this will only print the game that is focused, we should fix it to screenshot the right one i.e. red, blue, yellow...
def stampWindowPath(path, name):
	pyautogui.hotkey('alt', 'printscreen')
	sleep(.500)
	img = ImageGrab.grabclipboard()
	img.save(path+name, 'JPEG')
	
def sendCommand(comment):
	command = convertCommandInEnum(comment.text)
	if command == 1:	
		#press A
		pyautogui.keyDown(a)
		time.sleep(.250)
		pyautogui.keyUp(a)
		print("Button pressed: " + a)
	elif command == 2:
		#press Z
		pyautogui.keyDown(b)
		time.sleep(.250)
		pyautogui.keyUp(b)
		print("Button pressed: " + b)
	elif command == 3:
		#press I (UP)
		pyautogui.keyDown(up)
		time.sleep(.250)
		pyautogui.keyUp(up)
		print("Button pressed: " + up)
	elif command == 4:
		#press K (DOWN)
		pyautogui.keyDown(down)
		time.sleep(.250)
		pyautogui.keyUp(down)
		print("Button pressed: " + down)
	elif command == 5:
		#press J (LEFT)
		pyautogui.keyDown(left)
		time.sleep(.250)
		pyautogui.keyUp(left)
		print("Button pressed: " + left)
	elif command == 6:
		#press L (RIGHT)
		pyautogui.keyDown(right)
		time.sleep(.250)
		pyautogui.keyUp(right)
		print("Button pressed: " + right)
	elif command == 7:
		#press P (start)
		pyautogui.keyDown(start)
		time.sleep(.250)
		pyautogui.keyUp(start)
		print("Button pressed: " + start)
	elif command == 8:
		pyautogui.keyDown( select)
		time.sleep(.250)
		pyautogui.keyUp( select)
		print("Button pressed: " + select)

def stampWindow():
	keyboard.press_and_release("alt+print screen")		

def sendCommands(comment, n):
	for x in range(0, int(n)):
		sendCommand(comment)

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