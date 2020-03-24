import json
import datetime
from app.woo.woo import Woo
from app.woo.product import Product
from app.woo.category import Category
# from app.image.google_scrap import GoogleScrap
from app.controller.categories import CategoryController
from app.controller.products import ProductController

class WooMi:
    def __init__(self, woo, db, sourceType):
        self.woo = woo
        self.db = db
        self.type = sourceType
        self.allData = []

    def setupAPI(self):
        self.api = Woo(
            url=self.woo.get('url'),
            key=self.woo.get('key'),
            secret=self.woo.get('secret'),
            version=self.woo.get('version'),
        ).startAPI()
        return self.api

    def loadData(self):
        categories = CategoryController(self.type, self.db).loadCategories()
        products = ProductController(self.type, self.db).loadProducts(minimunStock=30)

        if categories:
            self.allData.append({
                'name': 'CATEGORY',
                'items': categories,
                'class': Category
            })

        if products:
            self.allData.append({
                'name': 'PRODUCT',
                'items': products,
                'class': Product
            })

        return self.allData

    def makeMigration(self):
        data = self.loadData()
        api = self.setupAPI()

        for item in data:
            newUpdates = []
            for index, info in enumerate(item['items']):
                try:
                    print(
                        '[ UPLOADING ]',
                        item.get('name'),
                        index,
                        'OF',
                        len(item['items']),
                        end="",
                        flush=True
                    )
                    classItem = item['class'](
                        api,
                        **info
                    )
                    send = classItem.makeRequest()
                    response = classItem.create(send)
                    if response:
                        newUpdates.append(response.json())
                        print(' - [ DONE ] -', info['name'], response)
                    else:
                        print(' - [ SKIP ] -', info['name'])
                except Exception as e:
                    print(' - [ ERROR ] -', info['name'], e)
            with open('{}.json'.format(item.get('name')), 'w') as fp:
                json.dump(newUpdates, fp)
