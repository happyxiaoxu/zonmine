import threading
import time
import gc
import pprint
import concurrent.futures

class BotScout(object):
    def __init__(self,job, as_obj, db_handler):
        self.as_obj = as_obj
        self.db_handler = db_handler
        self.job = job
        self.job.scout_results_counter = 0
        self.job.save()
        self.all_results = []
        return None

    def search(self, keyword, tries=0):
        results = self.as_obj.keyword_search(keyword,self.job,self.db_handler)
        if not results:
            if tries < 10:
                tries += 1
                return self.search(keyword, tries)
            else:
                print("Skipping Keyword: {} after trying 10 times".format(keyword))
        else:
            self.all_results = self.all_results + results
        return None

    def run(self):
        keywords = self.job.keylist.split("\r\n")
        print(keywords)
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(self.search, keywords)

        return None
