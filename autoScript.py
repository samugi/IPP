import utils
import time

def controller (commentsArray):
	#hwndMain = utils.main()#win32gui.FindWindow("Notepad", "Untitled - Notepad")
	#print(hwndMain) #you can use this to see main/parent Unique ID

	#hwndChild =  hwndMain #win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
	#win32gui.SetForegroundWindow(hwndChild)
	#print(hwndChild)  #you can use this to see sub/child Unique ID

	for comment in commentsArray:
		words = comment.text.split(" ")
		print(words[0])
		if len(words) > 2:
			print("More than two words")
			continue
		elif len(words) == 2:
			print("Two words")
			if words[0].isnumeric():
				if int(words[0]) <= 10:
					utils.sendCommands(words[1],words[0])
				continue
			continue
		elif len(words) == 1:
			print("One word")
			utils.sendCommand(words[0])
		time.sleep(.300)
	#print(temp) prints the returned value of temp, into the console
	#sleep(1) this waits 1 second before looping through again
	

