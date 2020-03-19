from woocommerce import API

class Woo:
    def __init__(self, url, key, secret, version="wc/v3"):
        self.url = url
        self.key = key
        self.secret = secret
        self.version = version

    def startAPI(self):
        self.api = API(
            url=self.url,
            consumer_key=self.key,
            consumer_secret=self.secret,
            version=self.version
        )
        return self.api
