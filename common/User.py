class User():
    def __init__(self, id, username, password, links=[]):
        self.id = id
        self.username = username
        self.password = password
        self.links = links

    def getLinks(self):
        return self.links

    def appendNewLink(self, link):
        self.links.append(link)

    def __repr__(self):
        return f"User(id='{self.id}')"

    def __str__(self):
        return f"User(id='{self.id}')"
