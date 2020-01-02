class Comment:

    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)