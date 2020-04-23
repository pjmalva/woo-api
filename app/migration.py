import json
import datetime
from app.woo.woo import Woo
from app.woo.product import Product
from app.woo.category import Category
# from app.image.google_scrap import GoogleScrap
from app.controller.categories import CategoryController
from app.controller.products import ProductController
import time

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

        with open('DATA/PRODUCT.json', 'r') as fp:
            products = json.load(fp)

        products = products[4488:]
        for index,item in enumerate(products):
            # time.sleep(1)
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

                if len(item['images']) == 0:
                    product = Product(api)
                    send = {'images': productController.getImage(item['name'])}
                    response = product.update(item['id'], send)
                    print(' - [ DONE ] -', item['name'], response)
                else :
                    print(' - [ SKIP ] -', item['name'])
            except Exception as e:
                print(' - [ ERROR ] -', item['name'], e)

    def updateProducts(self):
        api = self.setupAPI()
        productController = ProductController(self.type, self.db)
        productsStored = productController.processProductsStored()
        products = productController.loadProducts(minimunStock=0)

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

                if response is not None:
                    if (response.status_code < 300):
                        print(' - [ DONE ] -', product['name'])
                    else:
                        print(' - [ CHEKIT ] -', product['name'], response.content)
                else:
                    print(' - [ SKIP ] -', product['name'])
            except Exception as e:
                print(' - [ ERROR ] -', product['name'], e)

        # with open('DATA/PRODUCT.json', 'w') as fp:
        #     json.dump(newUpdates, fp)

    def listProducts(self):
        api = self.setupAPI()
        products = Product(api)

        page = 1
        fullStore = []
        result = products.listAll().json()
        while len(result) > 0:
            print("\rLoad All Product pages, it can took some time! Current Page is", page, end="", flush=True)
            page += 1
            fullStore += result
            result = products.listAll(page).json()
        print('')

        with open('DATA/PRODUCT.json', 'w') as fp:
            json.dump(fullStore, fp)

    def listCategories(self):
        api = self.setupAPI()
        categories = Category(api)

        page = 1
        fullStore = []
        result = categories.listAll().json()
        while len(result) > 0:
            print("\rLoad All Categories pages, it can took some time! Current Page is", page, end="", flush=True)
            page += 1
            fullStore += result
            result = categories.listAll(page).json()
        print('')

        with open('DATA/CATEGORY.json', 'w') as fp:
            json.dump(fullStore, fp)

    def updateCategories(self):
        api = self.setupAPI()
        productController = ProductController(self.type, self.db)
        productsStored = productController.processProductsStored()


