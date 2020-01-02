class Comment:

    def extractCommand(self, text):   
        if (text.find('*A*') != -1): 
            return "A"
        elif (text.find('*B*') != -1): 
            return "B"
        #TODO ecc...
        else :
            return None

    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.command = self.extractCommand(text)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)