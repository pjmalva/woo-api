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
            host=self.db.host,
            user=self.db.user,
            passwd=self.db.passwd,
            database=self.db.database
        ).updateCategories()
        return self.categories

    def formatCategories(self, categories):
        categoryiesFormated = []
        for category in categories:
            categoryiesFormated.append(
                self.getCategoryFields(category)
            )
        return categoryiesFormated

    def getCategoryFields(self, data):
        if self.type == 'csv':
            return self.getCategoryFieldsFromCsv(data)
        elif self.type == 'db':
            return self.getCategoryFieldsFromDB(data)

    def getCategoryFieldsFromCsv(self, category):
        return {
            "code": category[0].strip().replace('.', '-'),
            "name": category[1].strip()
        }

    def getCategoryFieldsFromDB(self, category):
        return {
            "code": category['stock'].strip().replace('.', '-'),
            "name": category['name'].strip()
        }

