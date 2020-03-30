import urllib.parse
import urllib.request
import json

# https://cse.google.com/cse/setup/basic?cx=005747464859247272350:toxcemvxn3s

class GoogleScrap:
    def __init__(self, search):
        self.search = search
        self.apiKey = 'AIzaSyChhj_83Kjz4LC3bMrH7MlrZzy5IJTS-sc'
        self.cxKey = '005747464859247272350:toxcemvxn3s'
        self.number = 1
        self.searchType = 'image'

    def searchImage(self):
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            data = {
                'key': self.apiKey,
                'cx': self.cxKey,
                'num': self.number,
                'searchType': self.searchType,
                'imgSize': 'medium',
                'q': self.search
            }

            uriEncoded = urllib.parse.urlencode(data, encoding="ascii")
            link = '{url}?{uri}'.format(url=url, uri=uriEncoded)
            res = urllib.request.urlopen(link)
            responseJson = json.loads(res.read())

            if not 'items' in responseJson:
                return None
            else:
                return {
                    "title": responseJson['items'][0]["title"],
                    "link": responseJson['items'][0]["link"]
                }
        except Exception as e:
            print(e)
            return None

# https://www.googleapis.com/customsearch/v1?key=&cx=005747464859247272350:toxcemvxn3s&num=1&searchType=image&imgSize=medium&q=VINHO%20DEL%20GRANO%201,48L%20TINTO%20SUAVE
# AIzaSyCxjVx14V9Nhk3jjS_fD4dlKkb7xtKqvD8
# AIzaSyBYpTRWyW-3fWLiVCHW7x5HfETAuk-u_tI
# AIzaSyAbXY5Mzdl19c0IFnQdY-aIiKVor1ZFZEo
# AIzaSyAcPiz_z2GYik8W8Y2BdjXivgUs_PNoemY
# AIzaSyAeeJIGdpqoMFskJUUJX0_n571_t692mUA
# AIzaSyB0-4MLVVncg3SOkPvurTb0GueGFt8G9oY

# AIzaSyDpuzwud4eXOzfdaeL4pYww5Dpb4g6PTpg
# AIzaSyAKa8U-FF-6T-rVfXilwU1b-_AtLY3zqkI
# AIzaSyChhj_83Kjz4LC3bMrH7MlrZzy5IJTS-sc
# AIzaSyCrmYV_TsQhZngV2gV6nNu7nwDZHXIUeX4
# AIzaSyDp-6XwgybXU5CgKT_S1sQs5c_PZLFuZM0
# AIzaSyAI6H3tXkuyiRj8uMsI_hkmujqkIaw1v6Q
# AIzaSyDucqI_9K5kQohH6ExIs5K_7oeycI5Er1I
