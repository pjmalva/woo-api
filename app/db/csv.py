import csv

class CSV:
    def __init__(self, path, newline='\n', delimiter=';'):
        self.path = path
        self.newline = newline
        self.delimiter = delimiter
        self.products = []

    def openCsv(self):
        with open(self.path, newline=self.newline, encoding='utf-8-sig') as file:
            self.csv_content = csv.reader(file, delimiter=self.delimiter)
            for row in self.csv_content:
                self.products.append(row)

    def getProducts(self):
        return self.products
