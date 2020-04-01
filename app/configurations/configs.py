import json

ENV_HOMO=0
ENV_PROD=1
ENVIROMENT=ENV_PROD

PATH_ENVS_FILE = {
    ENV_HOMO: 'config_test.json',
    ENV_PROD: 'config.json'
}

class Configurations:

    def __init__(self):
        try:
            file = open(PATH_ENVS_FILE[ENVIROMENT], 'r')
        except:
            new_file = open(PATH_ENVS_FILE[ENVIROMENT], 'x')
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
                    "url": "https://tita.miprojetos.com",
                    "key": "ck_29dfdbe96e04ea8205f32fa5fcf1672b5426698c",
                    "secret": "cs_5662975e194f3b3e21b76ade6123477d0e0ac92b",
                    "version": "wc/v3"
                },
                "granel": {}
            }""")
            new_file.close()
            file = open(PATH_ENVS_FILE[ENVIROMENT], 'r')
        self.config = json.load(file)

    def load(self):
        return self.config
