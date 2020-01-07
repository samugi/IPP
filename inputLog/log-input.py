path = "C:\Emulatore\inputLog\log"
fileName = "blue-red.js"

class Input:
   'Common base class for all employees'

   def __init__(self, username, inputType, id):
      self.username = username
      self.inputType = inputType
      self.id = id


def sendEventList(path, fileName, comments):
    f= open(path + "\\" + fileName,"w+")
    f.write("var commands=[")
    
    c1 = Input("fazzo", "UP", "1235")
    c2 = Input("aldomolla", "DOWN", "2729")
    c3 = Input("barisi", "5 A", "5ty7")
    c4 = Input("ted", "B", "123")
    c5 = Input("kumar", "DOWN", "3376829")
    c6 = Input("thalepalle", "5 A", "380228")
    c7 = Input("mizane", "UP", "18302")
    c8 = Input("sporcodiolio", "DOWN", "98765")
    c9 = Input("aldomolla2", "5 A", "25672892")
    c10 = Input("aldononmolla", "UP", "6489202")
    c11 = Input("aldomolla", "DOWN", "6789202")
    c12 = Input("barisi", "5 A", "121212")
    
    x = [c1,c2,c3,c4, c5, c6, c7, c8, c9, c10, c11, c12]
    
    for i in range(len(x)):
        f.write("{\"username\":\""+x[i].username+"\", \"command\" : \""+x[i].inputType+"\", \"id\" : \""+x[i].id+"\"},")
    f.write("{}]")
         
    f.close()      

sendEventList(path, fileName, "")