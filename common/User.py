class User():
    def __init__(self, user_id, username, password, links=""):
        self.id = user_id
        self.username = username
        self.password = password
        self.links = []
        # Make sure that input is a list
        if not isinstance(links, list):
            self.links.append(links)
        else:
            self.links = links

    def get_links(self):
        return self.links

    def append_new_link(self, link):
        self.links.append(link)

    def __repr__(self):
        return f"User(id='{self.id}')"

    def __str__(self):
        return f"User(id='{self.id}')"
