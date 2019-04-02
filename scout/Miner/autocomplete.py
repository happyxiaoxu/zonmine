import requests
import lxml.html
import datetime
import re
import string
import concurrent.futures

from urllib.parse import urlencode, quote
from scout.models import *
from scout.models import Keyword,Job
class AutoComplete(object):
    def __init__(self, scraper_obj):
        self.amazon_url = "https://www.amazon.com/"
        self.amazon_completion_url = "https://completion.amazon.com/api/2017/suggestions?"
        self.scraper_obj = scraper_obj
        self.autocomplete_keywords = []
        return None
    #
    def initialize_keywords(self, keywords):
        print("Initializing keywords")
        self.all_keywords = [kw + " " + alphabet for alphabet in list(string.ascii_lowercase) for kw in keywords]
        print("Total keywords to scrape: {}".format(len(self.all_keywords)))
        return None
    #
    def initialize_data(self):
        print("Initializing Data")
        data = {}
        req = self.scraper_obj.make_request(self.amazon_url)
        print("here")
        print(req)
        print(self.amazon_url)
        xml = lxml.html.fromstring(req.content)
        #
        q_var_str = xml.xpath('//script[contains(text(), "ue_sid") and contains(text(), "ue_id")]')[0].text
        #
        re_var_sid = r"ue_sid =\s*?'(.+)'"
        re_var_mid = r"ue_mid =\s*?'(.+)'"
        re_var_id = r"ue_id =\s*?'(.+)'"
        #
        data["q_var_sid"] = re.findall(re_var_sid, q_var_str)[0]
        data["q_var_mid"] = re.findall(re_var_mid, q_var_str)[0]
        data["q_var_id"] = re.findall(re_var_id, q_var_str)[0]
        self.data = data
        print(data)
        return None
    #
    def get_keywords(self, current_keyword):
        print("Getting autocomplete keywords for word: {}".format(current_keyword))
        query_params = {
            "page-type": "Gateway",
            "site-variant": "desktop",
            "client-info": "amazon-search-ui",
            "lop": "en_US",
            "alias": "aps",
            "suggestion-type": "keyword",
            "customer-id": "",
            "b2b": "0",
            "fb": "1",
            "fresh": "0",
            "session-id": self.data["q_var_sid"],
            "request-id": self.data["q_var_id"],
            "mid": self.data["q_var_mid"],
        }
        url = self.amazon_completion_url + urlencode(query_params) + "&&_={}".format(str(int(datetime.datetime.now().timestamp()*1000))) + "&prefix={}".format(quote(current_keyword))
        # print(url)
        kw_response = self.scraper_obj.make_request(url)
        print(kw_response)
        self.parse_response(kw_response)
        return None
    #
    def parse_response(self, response):
        if response.status_code == 200:
            for raw_kw in response.json()["suggestions"]:
                kw = raw_kw["value"]
                if kw not in self.autocomplete_keywords:
                    self.autocomplete_keywords.append(kw)
        print("Length of autocomplete keywords : {}".format(len(self.autocomplete_keywords)))
        return None
    #
    def run(self, base_keywords,job):
        self.initialize_data()
        self.initialize_keywords(base_keywords)
        job.refresh_from_db()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.get_keywords, self.all_keywords)
        # for kw in self.all_keywords:
        #     self.get_keywords(kw)
        print("Done getting autocomplete keywords!!")
        for foo in self.autocomplete_keywords:
            print(foo)
            keyword = Keyword(
                job_id=job.id,
                keyword=foo
            )
            keyword.save()
            keyword.refresh_from_db()
            job.search_results_counter += 1
            job.save()
            del([keyword])
        return self.autocomplete_keywords


# Mobile
# def get_similar(current_keyword):
#     query_params = {
#         "method": "completion",
#         "search-alias": "aps",
#         "client": "amazon-search-ui-mobile",
#         "mkt": "1",
#         "x": "String",
#         "sv": "mobile",
#         "l": "en_US",
#         "p": "exports-gateway-phone-web",
#         "q": quote(current_keyword),
#         "s": q_var_sid,
#         "r": q_var_id
#     }
#     url = amazon_completion_url + urlencode(query_params)
#     print(url)
#     return url