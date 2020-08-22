class Link():
    def __init__(self, address_name, categories=""):
<<<<<<< HEAD
=======
        self.id = id
>>>>>>> 4864c6f... fixup! Make list validation more clearer
        self.address_name = address_name
        # Make sure that input is a list
        if isinstance(categories, list):
            self.categories = categories
        else:
            self.categories = [categories]

    def get_categories(self):
        return self.categories

    def get_address_name(self):
        return self.address_name

    def append_new_category(self, category):
        self.categories.append(category)
