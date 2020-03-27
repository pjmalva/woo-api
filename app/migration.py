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
        products = ProductController(self.type, self.db).loadProducts(minimunStock=1)

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
                        '[ ADDING ]',
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

    def updateImages(self):
        api = self.setupAPI()
        productController = ProductController(None)

        with open('PRODUCT.json', 'r') as fp:
            products = json.load(fp)

        # products = products[1440:]
        for index,item in enumerate(products):
            try:
                print(
                    '[ UPDATING IMAGES ]',
                    'PRODUCT',
                    index,
                    'OF',
                    len(products),
                    end="",
                    flush=True
                )

                product = Product(api)

                send = {
                    'images': productController.getImage(item['name'])
                }

                response = product.update(item['id'], send)
                print(' - [ DONE ] -', item['name'], response)
            except Exception as e:
                print(' - [ ERROR ] -', item['name'], e)
        # print(products)

    def updateProducts(self):
        api = self.setupAPI()
        productController = ProductController(self.type, self.db)
        productsStored = productController.processProductsStored()
        products = productController.loadProducts(minimunStock=1)
        newUpdates = []

        # products = products[6159:]

        for index, product in enumerate(products):
            try:
                productStored = productsStored.get(product['sku'])

                print(
                    '[ UPDATING ]' if productStored else '[ ADDING ]',
                    'PRODUCTS',
                    index,
                    'OF',
                    len(products),
                    end="",
                    flush=True
                )

                productOBJ = Product(
                    api,
                    **product
                )

                send = productOBJ.makeRequest()

                if not productStored:
                    response = productOBJ.create(send)
                else:
                    response = productOBJ.update(productStored, send)

                if response:
                    newUpdates.append(response.json())
                    print(' - [ DONE ] -', product['name'], response)
                else:
                    print(' - [ SKIP ] -', product['name'])
            except Exception as e:
                print(' - [ ERROR ] -', product['name'], e)

        with open('PRODUCT.json', 'w') as fp:
            json.dump(newUpdates, fp)
