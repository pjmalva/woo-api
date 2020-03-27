import os
import csv

class CSV:
    def __init__(self, path, newline='\n', delimiter=';'):
        self.path = path
        self.newline = newline
        self.delimiter = delimiter
        self.registers = []

    def openCsv(self, file):
        content = []
        path = os.path.join(self.path, file)
        with open(path, newline=self.newline, encoding='utf-8-sig') as file:
            self.csv_content = csv.reader(file, delimiter=self.delimiter)
            for row in self.csv_content:
                content.append(row)
        return content

    def getProducts(self, minimunStock=1):
        self.registers = self.openCsv('PRODUCTS.csv')
        return self.registers

    def getCategories(self):
        self.registers = self.openCsv('CATEGORIES.csv')
        return self.registers
