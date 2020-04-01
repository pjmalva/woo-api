from app.db.csv import CSV
from app.db.star import StarTwo
from app.image.google_scrap import GoogleScrap
import json

class ProductController:
    def __init__(self, typeData, db=None):
        self.products = []
        self.type = typeData
        self.db = db

    def loadProducts(self, minimunStock=1):
        if self.type == 'csv':
            products = self.loadProductsFromCsv(minimunStock)
        elif self.type == 'db':
            products = self.loadProductsFromDB(minimunStock)

        self.products = self.formatProducts(products)
        return self.products

    def loadProductsFromCsv(self, minimunStock=1):
        csv_products = CSV(self.db.get('path'))
        products = csv_products.getProducts(minimunStock)
        return products

    def loadProductsFromDB(self, minimunStock=1):
        products = StarTwo(
            host=self.db.host,
            user=self.db.user,
            passwd=self.db.passwd,
            database=self.db.database
        ).updateProducts(minimunStock)
        return products

    def formatProducts(self, products):
        productsFormated = []
        for product in products:
            productsFormated.append(
                self.getProductFields(product)
            )
        return productsFormated

    def getProductFields(self, data):
        if self.type == 'csv':
            return self.getProductFieldsCsv(data)
        elif self.type == 'db':
            return self.getProductFieldsDB(data)

    def getProductFieldsCsv(self, product):
        stock = product[7]
        stock = stock.strip().replace('.','')
        return {
            "name": product[1].strip(),
            "sku": product[0].strip(),
            "regular_price": product[3].strip(),
            "sale_price": product[4].strip(),
            "description": product[1].strip(),
            "date_on_sale_from": product[5].strip(),
            "date_on_sale_to": product[6].strip(),
            "stock_quantity": int(float(stock[:-3] + '.' + stock[-3:])),
            "category_code": product[8].strip(),
            "category_name": product[9].strip(),
        }

    def getProductFieldsDB(self, product):
        return {
            "name": product['name'].strip(),
            "sku": product['reference'].strip(),
            "regular_price": product['price'].strip(),
            "sale_price": product['price_sale'].strip(),
            "description": product['name'].strip(),
            "date_on_sale_from": product['sale_start'].strip(),
            "date_on_sale_to": product['sale_finish'].strip(),
            "stock_quantity": int(product['stock']),
            "category_code": product['category_code'].strip(),
            "category_name": product['category_name'].strip(),
        }

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

    def getImage(self, name):
        image = GoogleScrap(name).searchImage()
        if image:
            return [
                {
                    'src': image['link'],
                    'name': image['title'],
                    'alt': name
                }
            ]

    def processProductsStored(self):
        productsStored = {}
        with open('DATA/PRODUCT.json', 'r') as products:
            productsJson = json.load(products)
            for product in productsJson:
                productsStored[product['sku']] = product['id']
        return productsStored


