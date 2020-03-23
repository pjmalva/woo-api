import json
import datetime
from app.db.star import StarTwo
from app.db.csv import CSV
from app.woo.woo import Woo
from app.woo.product import Product
from app.image.google_scrap import GoogleScrap

class WooMi:
    def __init__(self, woo, db, sourceType):
        self.woo = woo
        self.db = db
        self.type = sourceType

    def setupAPI(self):
        self.api = Woo(
            url=self.woo.get('url'),
            key=self.woo.get('key'),
            secret=self.woo.get('secret'),
            version=self.woo.get('version'),
        ).startAPI()
        return self.api

    def loadProducts(self):
        if self.type == 'csv':
            self.loadProductsFromCsv()
        elif self.type == 'db':
            self.loadProductsFromDB()
        return self.products

    def loadProductsFromCsv(self):
        csv_products = CSV(self.db.get('path'))
        csv_products.openCsv()
        self.products = csv_products.getProducts()
        return self.products

    def loadProductsFromDB(self):
        self.products = StarTwo(
            host=self.db.host,
            user=self.db.user,
            passwd=self.db.passwd,
            database=self.db.database
        ).updateProducts()
        return self.products

    def sendProduct(self, api, product):
        if self.type == 'csv':
            return self.sendProductCsv(api, product)
        elif self.type == 'db':
            return self.sendProductDB(api, product)

    def sendProductCsv(self, api, product):
        return Product(
            api,
            name=product[1],
            sku=product[0],
            regular_price=product[3],
            sale_price=product[4],
            description=product[1],
            date_on_sale_from=product[5],
            date_on_sale_to=product[6],
            stock_quantity=product[7],
        )

    def sendProductDB(self, api, product):
        return Product(
            api,
            name=product['name'],
            sku=product['reference'],
            regular_price=product['price'],
            sale_price=product['price_sale'],
            description=product['name'],
            date_on_sale_from=product['sale_start'],
            date_on_sale_to=product['sale_finish'],
            stock_quantity=product['stock'],
        )

    def getReference(self, product):
        if self.type == 'csv':
            return str(product[0])
        elif self.type == 'db':
            return str(product['reference'])

    def getStock(self, product):
        if self.type == 'csv':
            return float(product[7])
        elif self.type == 'db':
            return float(product['stock'])

    def makeMigration(self, onlyStockPositive=True, minimunStock=30):
        newProducts = []
        products = self.loadProducts()
        api = self.setupAPI()
        for index,product in enumerate(products):
            try:
                print('[ UPLOADING ] PRODUCT', index, 'OF', len(products), end="", flush=True)

                if onlyStockPositive and self.getStock(product) <= minimunStock:
                    print(' - [ NO STOCK ] -', self.getReference(product))
                    continue

                control = self.sendProduct(api, product)
                data = control.makeRequest()
                response = control.post(data)
                newProducts.append(response.json())
                print(' - [ DONE ] -', self.getReference(product), response)
            except Exception as e:
                print(' - [ ERROR ] -', self.getReference(product), e)
        with open('data-%s.json' % datetime.datetime.now(), 'w') as fp:
            json.dump(newProducts, fp)
