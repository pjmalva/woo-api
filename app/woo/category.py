class Category:
    def __init__(self):
        pass

    def setName(self, value):
        # Category name.MANDATORY
        self.name = value

    def setSlug(self, value):
        # An alphanumeric identifier for the resource unique to its type.
        self.slug = value

    def setParent(self, value):
        # The ID for the parent of the resource.
        self.parent = value

    def setDescription(self, value):
        # HTML description of the resource.
        self.description = value

    def setDisplay(self, value="default"):
        # Category archive display type.
        # Options: default, products, subcategories and both.
        # Default is default.
        self.display = value

    def setImage(self, value={}):
        # Image data. See Product category - Image properties
        # { src, name, alt }
        self.image = value

    def setMenuOrder(self, value):
        # Menu order, used to custom sort the resource.
        self.menu_order = value

