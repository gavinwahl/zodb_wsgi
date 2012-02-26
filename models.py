from persistent import Persistent

class User(Persistent):
    def __init__(self, username):
        self.username = username
        self.comments = []
        self.blogs = []

class Blog(Persistent):
    def __init__(self, user, text):
        self.user = user
        self.text = text
        self.user.blogs.append(self)
        self.user._p_changed = True
