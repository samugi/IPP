class Comment:

    def __init__(self, id, text):
        self._id = id
        self._text = text

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        print("called setter")

    @property
    def text(self):
        return self._text

    @property
    def id(self):
        return self._id