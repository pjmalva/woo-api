import argparse
import json
from app.migration import WooMi
from app.configurations.configs import Configurations

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
                    help='List all products and categories')

parser.add_argument('--list-all-pro',
                    action='store_true',
                    help='List all products')

parser.add_argument('--list-all-cat',
                    action='store_true',
                    help='List all categories')

print('INIT WOOMI')
print('LOAD CONFIGURATIONS')

config = Configurations().load()

migrate = WooMi(
    woo=config.get('woo'),
    db=config.get(config.get('type')),
    sourceType=config.get('type')
)

args = parser.parse_args()
if args.new:
    print('MIGRATING PRODUCTS')
    migrate.makeMigration()

if args.list_all_pro or args.list_all:
    print('LIST ALL PRODUCTS')
    migrate.listProducts()

if args.list_all_cat or args.list_all:
    print('LIST ALL CATEGORIES')
    migrate.listCategories()

if args.update:
    print('UPDATE PRODUCTS')
    migrate.updateProducts()

if args.pictures:
    print('MIGRATE IMAGES')
    migrate.updateImages()

# if args.category:
#    print('UPDATE PRODUCTS CATEGORES')
#    migrate.updateCategories()
