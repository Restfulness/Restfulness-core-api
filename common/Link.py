class Link():
    def __init__(self, address_name, categories=""):
        self.address_name = address_name
        self.categories = []
        # Make sure that input is a list
        if not isinstance(categories, list):
            self.categories.append(categories)
        else:
            self.categories = categories

    def get_categories(self):
        return self.categories

    def get_address_name(self):
        return self.address_name

    def append_new_category(self, category):
        self.categories.append(category)
