from app.star.db import StarTwo
from app.woo.woo import Woo
from app.woo.product import Product

class WooMi:
    def makeMigration(self):
        products = StarTwo(
            host="10.5.25.14",
            user="star",
            passwd="star",
            database="STAR"
        ).updateProducts()

        for product in products:
            woo = Woo(
                url="https://impresso.miprojetos.com",
                key="ck_795580178027ec011e443f1d4ce0e1a5f5a452cd",
                secret="cs_fce9bae63d668102234d443781b68c01e27e602e",
                version="wc/v3",
            ).startAPI()

            control = Product(
                woo,
                name=product['name'],
                sku=product['reference'],
                regular_price=product['price'],
                sale_price=product['price_sale'],
                description=product['name'],
                date_on_sale_from=product['sale_start'],
                date_on_sale_to=product['sale_finish'],
                stock_quantity=product['stock'],
            )

            data = control.makeRequest()
            print(data)
            response = control.post(data)
            print(response)
