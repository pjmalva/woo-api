from app.db.csv import CSV
from app.db.star import StarTwo

class CategoryController:
    def __init__(self, typeData, db=None):
        self.categories = []
        self.type = typeData
        self.db = db

    def loadCategories(self):
        if self.type == 'csv':
            categories = self.loadCategoriesFromCsv()
        elif self.type == 'db':
            categories = self.loadCategoriesFromDB()

        self.categories = self.formatCategories(categories)
        return self.categories

    def loadCategoriesFromCsv(self):
        csv_categories = CSV(self.db.get('path'))
        self.categories = csv_categories.getCategories()
        return self.categories

    def loadCategoriesFromDB(self):
        self.categories = StarTwo(
            host=self.db.get('host'),
            user=self.db.get('user'),
            passwd=self.db.get('passwd'),
            database=self.db.get('database')
        ).updateCategories()
        return self.categories

    def formatCategories(self, categories):
        categoriesFormated = []
        for category in categories:
            categoriesFormated.append(
                self.getCategoryFields(category)
            )
        return categoriesFormated

    def getCategoryFields(self, data):
        if self.type == 'csv':
            return self.getCategoryFieldsFromCsv(data)
        elif self.type == 'db':
            return self.getCategoryFieldsFromDB(data)

    def getCategoryFieldsFromCsv(self, category):
        return {
            "code": category[0].strip(),
            "name": category[1].strip()
        }

    def getCategoryFieldsFromDB(self, category):
        return {
            "code": category['category_code'].strip(),
            "name": category['category_name'].strip()
        }
