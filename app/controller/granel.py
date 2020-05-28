from app.configurations.configs import Configurations

class Granel:
    def __init__(self):
        config = Configurations().load()
        self.rules = config.get("granel")

    def checkAndConvert(self, category, product):
        rule = self.rules.get(product['sku'])
        if rule and rule['type'] == 'ref':
            return self.makeAjustmentsProduct(product, rule)

        rule = self.rules.get(category)
        if rule and rule['type'] == 'est' and self.isIncluded(product['sku'], rule.get('only')):
            return self.makeAjustmentsCategory(product, rule)

    def makeAjustmentsProduct(self, product, rule):
        if not 'KG' in product['name']: return product
        product['name'] = product['name'].replace('KG', 'UN')
        product['description'] = product['description'] + " / Valor do Quilo: R$" + product['regular_price']

        product['regular_price'] = self.calculateUN(product['regular_price'], rule['average'])

        if 'sale_price' in product:
            product['sale_price'] = self.calculateUN(product['sale_price'], rule['average'])

        return product

    def makeAjustmentsCategory(self, product, rule):
        product['name'] = product['name'].replace('KG', '{}GR'.format(rule['factor']))
        product['description'] = product['description'] + " / Valor do Quilo: R$" + product['regular_price']
        product['regular_price'] = self.calculateGR(product['regular_price'], rule['factor'])
        if 'sale_price' in product:
            product['sale_price'] = self.calculateGR(product['sale_price'], rule['factor'])
        return product

    def calculateUN(self, price, average):
        return str(float(price) * (average / 1000))

    def calculateGR(self, price, convertFactor):
        return str((float(price) * convertFactor )/1000)

    def isIncluded(self, sku, only):
        if only:
            return True if sku in only else False
        else:
            return True
