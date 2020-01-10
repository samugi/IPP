import utils
import time
from eventTracker import Input
import eventTracker
import os

def controller (commentsArray):
	#hwndMain = utils.main()#win32gui.FindWindow("Notepad", "Untitled - Notepad")
	#print(hwndMain) #you can use this to see main/parent Unique ID

	#hwndChild =  hwndMain #win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
	#win32gui.SetForegroundWindow(hwndChild)
	#print(hwndChild)  #you can use this to see sub/child Unique ID
	
	basePath = os.path.dirname(os.path.abspath(__file__))
	for comment in commentsArray:
		words = comment.text.split(" ")
		inp = Input(comment.username, utils.convertCommandInLanguage(comment.text), comment.id)
		print(words[0])
		if len(words) > 2:
			print("More than two words")
			continue
		elif len(words) == 2:
			print("Two words")
			if words[0].isnumeric():
				if int(words[0]) <= 10:
					eventTracker.sendEvent(basePath + "\\Server\\php\\IPP", utils.getFile(), inp) 
					utils.sendCommands(comment,words[0])
				continue
			continue
		elif len(words) == 1:
			print("One word")
			eventTracker.sendEvent(basePath + "\\Server\\php\\IPP", utils.getFile(), inp)
			utils.sendCommand(comment)
		time.sleep(.300)
	#print(temp) prints the returned value of temp, into the console
	#sleep(1) this waits 1 second before looping through again
	

