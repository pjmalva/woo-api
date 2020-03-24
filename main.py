from app.migration import WooMi
import json

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
migrate.makeMigration()
