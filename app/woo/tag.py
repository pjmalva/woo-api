class Tag:
    def __init__(self, api):
        self.api = api

    def setName(self, value):
        # Tag name.
        self.name = value

    def setSlug(self, value):
        # An alphanumeric identifier for the resource unique to its type.
        self.slug = value

    def setDescription(self, value):
        # HTML description of the resource.
        self.description = value

    def makeRequest(self):
        self.data = {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
        }
        return self.data

    def post(self, data=None):
        if not data: data = self.data
        self.response = self.api.post("products/tags", data)
