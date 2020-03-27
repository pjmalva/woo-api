import argparse
import json
from app.migration import WooMi

parser = argparse.ArgumentParser(description='API Woocommerce Mitrix')

parser.add_argument('--new',
                    action='store_true',
                    help='New product migration')

parser.add_argument('--pictures',
                    action='store_true',
                    help='New product images')

parser.add_argument('--update',
                    action='store_true',
                    help='Update all products')

parser.add_argument('--update-image',
                    action='store_true',
                    help='Update all products images')

parser.add_argument('--list-all',
                    action='store_true',
                    help='List all products')

print('INIT WOOMI')
print('LOAD CONFIGURATIONS')

try:
    file = open('config.json', 'r')
except:
    new_file = open('config.json', 'x')
    new_file.write("""{
        "type": "csv",
        "csv": {
            "path": "C:/Users/Rafael/Downloads/teste-2.csv",
            "newline": "\\n",
            "delimiter": ";"
        },
        "db": {
            "host": "10.5.25.14",
            "user": "star",
            "passwd": "star",
            "database": "STAR"
        },
        "woo": {
            "url": "https://pj.miprojetos.com",
            "key": "ck_e83efd304aa24eb3ae484b88b51ced1037823566",
            "secret": "cs_0d809927c43837e5d240cb689f32ef0858ea725c",
            "version": "wc/v3"
        }
    }""")
    new_file.close()
    file = open('config.json', 'r')

config = json.load(file)

migrate = WooMi(
    woo=config.get('woo'),
    db=config.get(config.get('type')),
    sourceType=config.get('type')
)

args = parser.parse_args()
if args.new:
    print('MIGRATING PRODUCTS')
    migrate.makeMigration()

if args.list_all:
    print('LIST ALL PRODUCTS')
    migrate.listProducts()

if args.update:
    print('UPDATE PRODUCTS')
    migrate.updateProducts()

if args.pictures:
    print('MIGRATE IMAGES')
    migrate.updateImages()

if args.category:
    print('UPDATE PRODUCTS CATEGORES')
    migrate.updateCategories()
