class Link():
    def __init__(self, addressName, categories=[]):
        self.addressName = addressName
        self.categories = categories

    def getCategories(self):
        return self.categories

    def getAddressName(self):
        return self.addressName

    def appendNewCategory(self, category):
        self.categories.append(category)