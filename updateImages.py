from app.migration import WooMi
import json

print('INIT WOOMI')
print('LOAD CONFIGURATIONS')

file = open('config.json', 'r')
config = json.load(file)

print('UPDATE IMAGES')

migrate = WooMi(
    woo=config.get('woo'),
    db=config.get(config.get('type')),
    sourceType=config.get('type')
)

migrate.updateImages()
