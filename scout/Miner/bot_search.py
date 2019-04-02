import threading
import time
import gc
class BotSearch(object):
    def __init__(self,job,ac_obj,db_handler):
        self.job = job
        self.ac_obj = ac_obj
        self.db_handler = db_handler
        self.job.search_results_counter = 0
        self.job.save()
        return None

    def search(self):
        keywords = self.job.keywords.split("\r\n")
        th = threading.Thread(target=lambda: self.ac_obj.run(keywords,self.job), daemon=True)
        th.start()
        th.join()
        time.sleep(10)
        gc.collect()
        del([keywords,th])
        return None
