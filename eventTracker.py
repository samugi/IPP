class Input:

   def __init__(self, username, inputType, id):
      self.username = username
      self.inputType = inputType
      self.id = id


def sendEvent(path, fileName, inp):
    f= open(path + "\\" + fileName,"r+")
    lines = f.readlines()
    f.close()
    f= open(path + "\\" + fileName,"w+")
    index = 0
    for l in lines:
        index = index +1
        if index < len(lines)-1:
            f.write(l)
        elif index == len(lines)-1:
            f.write(l.replace("\n", "")+",\n")
    f.write("{\"username\":\""+inp.username+"\", \"command\" : \""+inp.inputType+"\", \"id\" : \""+inp.id+"\"}\n]") 
    f.close()    