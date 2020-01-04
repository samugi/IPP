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

    @property
    def text(self):
        return self._text

    @property
    def id(self):
        return self._id
    


    @property
    def likeCount(self):
        return self._likeCount

    @likeCount.setter
    def likeCount(self, value):
        self._likeCount = value
    
    @property
    def repliesCount(self):
        return self._repliesCount

    @repliesCount.setter
    def repliesCount(self, value):
        self._repliesCount = value
    
    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value