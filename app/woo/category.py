from app.woo.api import BaseAPI

class Category(BaseAPI):
    def __init__(self, api, **kwargs):
        self.api = api
        self.data = {}
        self.setName(kwargs.get('name'))
        self.setSlug(kwargs.get('slug'))
        self.setParent(kwargs.get('parent'))
        self.setDescription(kwargs.get('description'))
        self.setDisplay(kwargs.get('display'))
        self.setImage(kwargs.get('image'))
        self.setMenuOrder(kwargs.get('menu_order'))

    def setName(self, value):
        # Category name.MANDATORY
        if not value: value = ""
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

    def makeRequest(self):
        if self.name:
            self.data['name'] = self.name

        if self.slug:
            self.data['slug'] = self.slug

        if self.parent:
            self.data['parent'] = self.parent

        if self.description:
            self.data['description'] = self.description

        if self.display:
            self.data['display'] = self.display

        if self.image:
            self.data['image'] = self.image

        if self.menu_order:
            self.data['menu_order'] = self.menu_order

        return self.data

    def create(self, data=None):
        return self.post("products/categories", data)

    def update(self, id, data=None):
        return self.put("products/categories/{0}".format(id), data)

    def select(self, id):
        return self.get("products/categories/{0}".format(id))

    def remove(self, id):
        return self.delete("products/categories/{0}".format(id))

    def listAll(self, page=1):
        arguments = {
            'params': {
                'page': str(page),
                'per_page': '20'
            }
        }
        return self.get("products/categories", arguments)
