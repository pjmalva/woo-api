class CategoriesTree:
    def __init__(self, data, tree={}):
        self.rawData = data
        self.tree = tree

    def mountCategory(self, category, structure):
        self.tree[category] = {
            'code': structure['code'],
            'name': structure['name'],
            'display': 'default',
            'items': {},
        }

    def mountSubcategory(self, category, subcategory, structure):
        if not category in self.tree:
            self.mountCategory(category, {
                'code': category,
                'name': 'category {} auto created'.format(category)
            })

        self.tree[category]['items'][subcategory] = {
            'code': structure['code'],
            'name': structure['name'],
            'display': 'subcategories',
            'items': {},
        }

    def mountProduct(self, category, subcategory, product, structure):
        if not category in self.tree:
            self.mountCategory(category, {
                'code': category,
                'name': 'category {} auto created'.format(category)
            })

        if not subcategory in self.tree[category]['items']:
            self.mountSubcategory(category, subcategory, {
                'code': category,
                'name': 'subcategory {} auto created'.format(subcategory)
            })

        self.tree[category]['items'][subcategory]['items'][product] = {
            'code': structure['code'],
            'name': structure['name'],
            'display': 'products',
            'items': {},
        }

    def prepareStructure(self, structure):
        code = structure['code'].split('.')

        if not code[0].isnumeric(): return None
        sizeCode = len(code)

        if sizeCode == 1:
            self.mountCategory(code[0], structure)
        elif sizeCode == 2:
            self.mountSubcategory(code[0], code[1], structure)
        elif sizeCode == 3:
            self.mountProduct(code[0], code[1], code[2], structure)

    def mountTree(self):
        for item in self.rawData:
            self.prepareStructure(item)
        return self.tree

    def search(self, category):
        code = category.split('.')
        sizeCategory = len(code)

        categoryFounded = None

        if sizeCategory == 1:
            categoryFounded = self.tree.get(code[0])
        elif sizeCategory == 2:
            categoryFounded = self.tree.get(code[0])
            categoryFounded = categoryFounded['items'].get(code[1])
        elif sizeCategory == 3:
            categoryFounded = self.tree.get(code[0])
            categoryFounded = categoryFounded['items'].get(code[1])
            categoryFounded = categoryFounded['items'].get(code[2])

        return categoryFounded


