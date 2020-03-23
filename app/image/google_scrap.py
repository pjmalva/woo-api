import urllib
from apiclient.discovery import build

class GoogleScrap:
    def __init__(self, search):
        self.search = search

    def searchImage(self):
        self.service = build(
            "customsearch",
            "v1",
            developerKey="AIzaSyAcPiz_z2GYik8W8Y2BdjXivgUs_PNoemY"
        )

        try:
            res = self.service.cse().list(
                q=self.search,
                cx='005747464859247272350:toxcemvxn3s',
                searchType='image',
                num=1
            ).execute()
        except:
            res = {}

        if not 'items' in res:
            return None
        else:
            return {
                "title": res['items'][0]["title"],
                "link": res['items'][0]["link"]
            }
