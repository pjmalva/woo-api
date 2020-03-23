class BaseAPI:
    def __init__(self, api):
        self.api = api
        self.response = None

    def post(self, uri, data=None, json=False):
        self.response = self.api.post(uri, data)
        return self.response if not json else self.response.json()

    def put(self, uri, data=None, json=False):
        self.response = self.api.put(uri, data)
        return self.response if not json else self.response.json()

    def get(self, uri, json=False):
        return self.response if not json else self.response.json()

    def delete(self, uri, json=False):
        self.response = self.api.delete(uri, params={"force": True})
        return self.response if not json else self.response.json()
