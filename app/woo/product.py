# from app.image.google_scrap import GoogleScrap
import json

from app.woo.api import BaseAPI
from app.controller.granel import Granel
from datetime import datetime, timedelta

class Product(BaseAPI):
    def __init__(self, api, **kwargs):
        self.api = api
        self.data = {}
        self.category = {}
        self.minimun_stock = kwargs.get('minimun_stock', 1)

        self.setName(kwargs.get('name'))
        self.setSku(kwargs.get('sku'))
        self.setType(kwargs.get('type'))
        self.setStatus(kwargs.get('status'))
        self.setFeatured(kwargs.get('featured'))
        self.setCatalogVisibility(kwargs.get('catalog_visibility'))
        self.setRegularPrice(kwargs.get('regular_price'))
        self.setSalePrice(kwargs.get('sale_price'))
        self.setDescription(kwargs.get('description'))
        self.setShortDescription(kwargs.get('short_description'))
        self.setDateOnSaleFrom(kwargs.get('date_on_sale_from'))
        # self.setDateOnSaleFromGMT(kwargs.get('date_on_sale_from_gmt'))
        self.setDateOnSaleTo(kwargs.get('date_on_sale_to'))
        # self.setDateOnSaleToGMT(kwargs.get('date_on_sale_to_gmt'))
        self.setVirtual(kwargs.get('virtual'))
        self.setDownloadable(kwargs.get('downloadable'))
        self.setStockQuantity(kwargs.get('stock_quantity'))
        self.setManageStock(kwargs.get('manage_stock'))
        # self.setStockStatus(kwargs.get('stock_status'))
        self.setCategories(kwargs.get('categories'))
        self.setTags(kwargs.get('tags'))
        self.setImages(kwargs.get('images'))
        self.setAttributes(kwargs.get('attributes'))
        self.setDefaultAttributes(kwargs.get('default_attributes'))
        self.setCategoryCode(kwargs.get('category_code'))
        self.setCategoryName(kwargs.get('category_name'))

    def setName(self, value):
        self.name = value

    def setSku(self, value):
        # Unique identifier.
        self.sku = str(value)

    def setType(self, value="simple"):
        # Product type. Options: simple, grouped, external and variable.
        # Default is simple.
        if not value: value = "simple"
        self.type = value

    def setStatus(self, value="publish"):
        # Product status (post status).
        # Options: draft, pending, private and publish.
        # Default is publish.
        if not value: value = "publish"
        self.status = value

    def setFeatured(self, value=False):
        # Featured product. Default is false.
        if not value: value = False
        self.featured = value

    def setCatalogVisibility(self, value="visible"):
        # Catalog visibility. Options: visible, catalog, search and hidden.
        # Default is visible.
        if not value: value = "visible"
        self.catalog_visibility = value

    def setRegularPrice(self, value="0"):
        # Product regular price.
        if not value: value = "0"
        self.regular_price = str(value)

    def setSalePrice(self, value="0"):
        # Product sale price.
        if not value: value = "0"
        self.sale_price = str(value)

    def setDescription(self, value):
        self.description = value

    def setShortDescription(self, value):
        self.short_description = value

    def setDateOnSaleFrom(self, value):
        # Start date of sale price, in the site's timezone.
        if value in ['1753-01-01 00:00:00.000', None]:
            self.date_on_sale_from = None
            self.date_on_sale_from_gmt = None
        else:
            self.date_on_sale_from = str(value)
            self.date_on_sale_from_gmt = "-03:00"

    def setDateOnSaleFromGMT(self, value="-03:00"):
        # Start date of sale price, as GMT.
        if not value: value = "-03:00"
        self.date_on_sale_from_gmt = value

    def setDateOnSaleTo(self, value):
        # End date of sale price, in the site's timezone.
        if value in ['1753-01-01 00:00:00.000', None]:
            self.date_on_sale_to = None
            self.date_on_sale_to_gmt = None
        else:
            base_date = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S.%f")
            end_date = base_date + timedelta(days=1)
            self.date_on_sale_to = end_date.strftime('%Y-%m-%d')
            self.date_on_sale_to_gmt = "-03:00"

    def setDateOnSaleToGMT(self, value="-03:00"):
        # End date of sale price, as GMT.
        if not value: value = "-03:00"
        self.date_on_sale_to_gmt = value

    def setVirtual(self, value=False):
        # If the product is virtual.
        # Default is false.
        if not value: value = False
        self.virtual = value

    def setDownloadable(self, value=False):
        # If the product is downloadable.
        # Default is false.
        if not value: value = False
        self.downloadable = value

    def setStockQuantity(self, value=0):
        if not value: value = 0
        self.stock_quantity = str(value)
        self.setStockStatus(
            "instock" if value >= self.minimun_stock else "outofstock"
        )

    def setManageStock(self, value):
        if not value: value = True
        self.manage_stock = value

    def setStockStatus(self, value="instock"):
        # Controls the stock status of the product.
        # Options: instock, outofstock, onbackorder.
        # Default is instock.
        if not value: value = "instock"
        self.stock_status = value

    def setCategories(self, value=[]):
        # Array { 'id': category_id }
        # if not value: return
        self.categories = value

    def setTags(self, value=[]):
        # Array { 'id': tag_id }
        # if not value: return
        self.tags = value

    def setImages(self, value=[]):
        # Array { 'src': image_src, 'name': image_name, 'alt': image_alt }
        # if not value: return
        self.images = value

    def setAttributes(self, value=[]):
        # if not value: return
        self.attributes = value

    def setDefaultAttributes(self, value=[]):
        # if not value: return
        self.default_attributes = value

    def setCategoryCode(self, value):
        self.category['code'] = value

    def setCategoryName(self, value):
        self.category['name'] = value

    def searchCategory(self):
        with open('DATA/CATEGORY.json', 'r') as f:
            categories = json.load(f)
            for item in categories:
                if item['name'] == self.category['name']:
                    return { "id": item['id'] }

    def makeRequest(self):
        if self.name:
            self.data["name"] = self.name

        if self.sku:
            self.data["sku"] = self.sku

        if self.type:
            self.data["type"] = self.type

        if self.status:
            self.data["status"] = self.status

        if self.featured:
            self.data["featured"] = self.featured

        if self.catalog_visibility:
            self.data["catalog_visibility"] = self.catalog_visibility

        if self.regular_price:
            self.data["regular_price"] = self.regular_price

        if self.sale_price and float(self.sale_price) > 0:
            self.data["sale_price"] = self.sale_price

        if self.description:
            self.data["description"] = self.description

        if self.short_description:
            self.data["short_description"] = self.short_description

        if self.date_on_sale_from:
            self.data["date_on_sale_from"] = self.date_on_sale_from

        if self.date_on_sale_from_gmt:
            self.data["date_on_sale_from_gmt"] = self.date_on_sale_from_gmt

        if self.date_on_sale_to:
            self.data["date_on_sale_to"] = self.date_on_sale_to

        if self.date_on_sale_to_gmt:
            self.data["date_on_sale_to_gmt"] = self.date_on_sale_to_gmt

        if self.virtual:
            self.data["virtual"] = self.virtual

        if self.downloadable:
            self.data["downloadable"] = self.downloadable

        if self.manage_stock:
            self.data["manage_stock"] = self.manage_stock

        if self.stock_quantity:
            self.data["stock_quantity"] = self.stock_quantity

        if self.stock_status:
            self.data["stock_status"] = self.stock_status

        if self.categories:
            self.data["categories"] = self.categories
        else:
            category = self.searchCategory()
            if category: self.data["categories"] = [ category ]

        if self.tags:
            self.data["tags"] = self.tags

        if self.images:
            self.data["images"] = self.images

        if self.attributes:
            self.data["attributes"] = self.attributes

        if self.default_attributes:
            self.data["default_attributes"] = self.default_attributes

        return Granel().checkAndConvert(self.category['code'], self.data)

    def outOfStock(self):
        return self.stock_status == "outofstock"

    def create(self, data=None):
        if not self.outOfStock():
            return self.post("products", data)

    def createUpdate(self, data=None):
        return self.post("products", data)

    def update(self, id, data=None):
        return self.put("products/{0}".format(id), data)

    def select(self, id):
        return self.get("products/{0}".format(id))

    def remove(self, id):
        return self.delete("products/{0}".format(id))

    def listAll(self, page=1):
        arguments = {
            'params': {
                'page': str(page),
                'per_page': '20'
            }
        }
        return self.get("products", arguments)
