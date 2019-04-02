# Grepwords Api to get keyword data from google 

import requests
import json
import pprint
from scout.Miner.config import Config


class KeywordsApi(object):
    def __init__(self):
        return None
    #
    def parse_response(self, resp, keywords):
        print("Parsing response")
        results = {}
        data = resp.json()
        pprint.pprint(data)
        for word in keywords:
            print(word)
            if data:
                for kw_data in data:
                    if not kw_data.get("error"):
                        results[word] = next(([kw_data["cpc"], kw_data["lms"], kw_data["competition"]] for kw_data in data if kw_data["keyword"] == word), ["-", "-", "-"])
                    else:
                        results[word] = ["-", "-", "-"]
        return results
    #
    def get_stats(self, keywords):
        keywords_string = "|".join(keywords)
        kw_resp = requests.get(Config.gw_api_url.format(keywords_string))
        results = self.parse_response(kw_resp, keywords)
        return results



# alpha = KeywordsApi()
# results = alpha.get_stats(["fidget spinner", "fidget", "messi"])

