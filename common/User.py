class User():
    def __init__(self, userId, username, password, links=""):
        self.id = userId
        self.username = username
        self.password = password
        self.links = []        
        # Make sure that input is a list
        if not isinstance(links, list):
            self.links.append(links)
        else:
            self.links = links        

    def getLinks(self):
        return self.links

    def appendNewLink(self, link):
        self.links.append(link)

    def __repr__(self):
        return f"User(id='{self.id}')"

    def __str__(self):
        return f"User(id='{self.id}')"
