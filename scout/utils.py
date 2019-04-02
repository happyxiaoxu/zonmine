import threading
from scout.Miner import amazon_scraper,csv_handler,excel,autocomplete,scraper
from scout.db_handler import DbHandler
from collections import OrderedDict
from scout.Miner import bot_scout,bot_search
import gc


# def search(keyword, tries=0):
#     results = as_obj.keyword_search(keyword)
#     if not results:
#         if tries < 10:
#             tries += 1
#             return search(keyword, tries)
#         else:
#             print("Skipping Keyword: {} after trying 10 times".format(keyword))
#     else:
#         all_results = all_results + results
#     return None
# # while not r:
# #     # r = as_obj.keyword_search("fidget spinner")
# #     r = as_obj.keyword_search("flip case")
# with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#     executor.map(search, all_keywords)
#
# print(all_results[0])
# pprint.pprint(str(all_results[0].__dict__).encode())
# output = [OrderedDict(i.__dict__) for i in all_results]
# # csv_handler.generate_csv(output)
# excel.download_file(output)

def start_search(job_id):
    db_handler = DbHandler()
    proxies = db_handler.get_proxies()
    scraper_obj = scraper.Scraper(proxies)

    job_obj = db_handler.get_job_by_id(job_id)
    ac_obj = autocomplete.AutoComplete(scraper_obj)
    sh_obj = bot_search.BotSearch(job_obj,ac_obj,db_handler)
    search_thread = threading.Thread(target=sh_obj.search, daemon=True)
    search_thread.start()
    search_thread.join()

    job_obj.refresh_from_db()
    job_obj.search_status = False
    job_obj.save()

    print(dir())
    del ([sh_obj, job_obj, search_thread, ac_obj,db_handler,proxies,scraper_obj])
    gc.collect()
    print(dir())
    return None
def start_scout(job_id):
    db_handler = DbHandler()
    proxies = db_handler.get_proxies()
    scraper_obj = scraper.Scraper(proxies)

    job_obj = db_handler.get_job_by_id(job_id)
    as_obj = amazon_scraper.AmazonScraper(scraper_obj)
    st_obj = bot_scout.BotScout(job_obj, as_obj, db_handler)
    scout_thread = threading.Thread(target=st_obj.run, daemon=True)
    scout_thread.start()
    scout_thread.join()

    job_obj.scout_status = False
    job_obj.save()
    job_obj.refresh_from_db()

    print(dir())
    del ([st_obj, job_obj, scout_thread, as_obj, db_handler, proxies, scraper_obj])
    gc.collect()
    print(dir())

    return None