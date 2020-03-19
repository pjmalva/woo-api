class Product:
    def __init__(self, api, **kwargs):
        self.api
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
        self.setDateOnSaleFromGMT(kwargs.get('date_on_sale_from_gmt'))
        self.setDateOnSaleTo(kwargs.get('date_on_sale_to'))
        self.setDateOnSaleToGMT(kwargs.get('date_on_sale_to_gmt'))
        self.setVirtual(kwargs.get('virtual'))
        self.setDownloadable(kwargs.get('downloadable'))
        self.setStockQuantity(kwargs.get('stock_quantity'))
        self.setStockStatus(kwargs.get('stock_status'))
        self.setCategories(kwargs.get('categories'))
        self.setTags(kwargs.get('tags'))
        self.setImages(kwargs.get('images'))
        self.setAttributes(kwargs.get('attributes'))
        self.setDefaultAttributes(kwargs.get('default_attributes'))

    def setField(self, field, value):
        self[field] = value

    def setName(self, value):
        self.name = value

    def setSku(self, value):
        # Unique identifier.
        self.sku = value

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
        self.regular_price = value

    def setSalePrice(self, value="0"):
        # Product sale price.
        if not value: value = "0"
        self.sale_price = value

    def setDescription(self, value):
        self.description = value

    def setShortDescription(self, value):
        self.short_description = value

    def setDateOnSaleFrom(self, value):
        # Start date of sale price, in the site's timezone.
        self.date_on_sale_from = value

    def setDateOnSaleFromGMT(self, value="-03:00"):
        # Start date of sale price, as GMT.
        if not value: value = "-03:00"
        self.date_on_sale_from_gmt = value

    def setDateOnSaleTo(self, value):
        # End date of sale price, in the site's timezone.
        self.date_on_sale_to = value

    def setDateOnSaleToGMT(self, value="-03:00"):
        # End date of sale price, as GMT.
        if not value: value = "-03:00"
        self.date_on_sale_to_gmt = value

    def setVirtual(self, value=False):
        # If the product is virtual. Default is false.
        if not value: value = False
        self.virtual = value

    def setDownloadable(self, value=False):
        # If the product is downloadable. Default is false.
        if not value: value = False
        self.downloadable = value

    def setStockQuantity(self, value=0):
        if not value: value = 0
        self.stock_quantity = value
        self.setStockStatus(
            "outofstock" if self.stock_quantity == 0 else "instock"
        )

    def setStockStatus(self, value="instock"):
        # Controls the stock status of the product.
        # Options: instock, outofstock, onbackorder.
        # Default is instock.
        if not value: value = []
        self.stock_status = value

    def setCategories(self, value=[]):
        # Array { 'id': category_id }
        if not value: value = []
        self.categories = value

    def setTags(self, value=[]):
        # Array { 'id': tag_id }
        if not value: value = []
        self.tags = value

    def setImages(self, value=[]):
        # Array { 'src': image_src, 'name': image_name, 'alt': image_alt }
        if not value: value = []
        self.images = value

    def setAttributes(self, value=[]):
        if not value: value = []
        self.attributes = value

    def setDefaultAttributes(self, value=[]):
        if not value: value = []
        self.default_attributes = value

    def makeRequest(self):
        self.data = {
            "name": self.name,
            "sku": self.sku,
            "type": self.type,
            "status": self.status,
            "featured": self.featured,
            "catalog_visibility": self.catalog_visibility,
            "regular_price": self.regular_price,
            "sale_price": self.sale_price,
            "description": self.description,
            "short_description": self.short_description,
            "date_on_sale_from": self.date_on_sale_from,
            "date_on_sale_from_gmt": self.date_on_sale_from_gmt,
            "date_on_sale_to": self.date_on_sale_to,
            "date_on_sale_to_gmt": self.date_on_sale_to_gmt,
            "virtual": self.virtual,
            "downloadable": self.downloadable,
            "stock_quantity": self.stock_quantity,
            "stock_status": self.stock_status,
            "categories": self.categories,
            "tags": self.tags,
            "images": self.images,
            "attributes": self.attributes,
            "default_attributes": self.default_attributes,
        }
        return self.data

    def post(self, data=None):
        if not data: data = self.data
        self.response = self.api.post("products", data).json()
