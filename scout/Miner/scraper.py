#Base Class Scraper
# import random
import requests
import threading
import time
from requests.auth import HTTPProxyAuth
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
from requests.packages.urllib3.exceptions import ProxyError
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError
from requests.packages.urllib3.exceptions import ProxyError


from random_useragent.random_useragent import Randomize

# ""
# from .config import Config
from config import Config
# from scout import db_handler

# #####################################################################################
# # Custom method to get first element or empty element by xpath
# def xpath_first(self, elm_xpath):
#     elements = self.xpath(elm_xpath)
#     return next(iter(elements), lxml.html.HtmlElement())

# lxml.html.HtmlElement.xpath_first = xpath_first
def pause(self, pause=True):
    pause_time = Config.pause_time_max
    print("Service not available. Pausing for: {}s".format(pause_time))
    if pause:
        self.active = False
        threading.Timer(pause_time, self.pause, [False]).start()
    else:
        self.active = True
    return None

# Disable Warnings
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)
requests.Session.active = True
requests.Session.pause = pause
requests.Session.requests_count = 0

# #####################################################################################

class Scraper(object):
    def __init__(self, proxies):
        self.proxies = proxies
        self.ip_check_urls = ["https://wtfismyip.com/json", "https://wtfismyip.com/json"]
        self.r_agent = Randomize()
        self.sessions = self.prepare_sessions()
        return None
    #
    def get_ip_details(self, session):
        for url in self.ip_check_urls:
            check_ip = session.get(url)
            if check_ip.status_code == 200:
                print(check_ip.text)
                break
        return None
    #
    # def prepare_sessions(self):
    #     print("Initializing Scraper and Preparing Sessions")
    #     sessions = []
    #     for session_count in range(15):
    #         proxy_host = "proxy.crawlera.com"
    #         proxy_port = "8010"
    #         proxy_auth = "f7115f81a6444eeab4003ac4a668f3ee:" # Make sure to include ':' at the end
    #         proxy = {
    #                 "https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
    #                 "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
    #             }
    #         _session = requests.Session()
    #         _session.headers["User-Agent"] = self.r_agent.random_agent('desktop','windows')
    #         print(_session.headers["User-Agent"])
    #         _session.proxies = proxy
    #         # Requests counter is good for assessing proxy quality.
    #         _session.requests_count = 0
    #         sessions.append(_session)
    #     del([proxy, _session])
    #     return sessions
    # #
    def prepare_sessions(self):
        print("Initializing Scraper and Preparing Sessions")
        # http_proxy  = "http://194.62.145.248:8080"
        # https_proxy  = "https://194.62.145.248:8080"
        proxies = self.proxies
        sessions = []
        # print(proxies)
        for each_proxy in proxies:
            proxy = {
                        "http"  : "http://{}".format(each_proxy), 
                        "https" : "https://{}".format(each_proxy)
                    }
            _session = requests.Session()
            # Add code to change User Agents in the future.
            # _session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3205.0 Safari/537.36" 
            _session.headers["User-Agent"] = self.r_agent.random_agent('desktop','windows')
            # print(_session.headers["User-Agent"])
            _session.proxies = proxy
            # Requests counter is good for assessing proxy quality.
            _session.requests_count = 0
            # self.get_ip_details(_session)
            sessions.append(_session)
        del([proxies, each_proxy, proxy, _session])
        return sessions
    #
    def get_best_session(self):
        filtered_sessions = list(filter(lambda x:x.active, self.sessions))
        best_session = min(filtered_sessions, key=lambda session:session.requests_count)
        del([filtered_sessions])
        return best_session
    #
    def make_request(self, url, method="GET", headers={}, data={}, request_error=False):
        _response = None
        current_session = self.get_best_session()
        # print(current_session, current_session.requests_count, url)
        print(current_session.requests_count, url)
        # print(current_session.headers["User-Agent"])
        # headers["User-Agent"] = self.r_agent.random_agent('desktop','windows')
        # headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
        current_session.requests_count += 1
        try:
            if method == "GET":
                # _response = current_session.get(url, timeout=15, verify="crawlera-ca.crt")
                _response = current_session.get(url, timeout=5, headers=headers, auth=HTTPProxyAuth('bbercaw10', 'RU9EFHLx'))
            elif method == "POST":
                # _response = current_session.post(url, timeout=15, verify="crawlera-ca.crt")
                _response = current_session.post(url, timeout=5, headers=headers, auth=HTTPProxyAuth('bbercaw10', 'RU9EFHLx'))
            if _response:
                # Filter out responses
                if _response.status_code == 503:
                    # Sleep for some random time before making the next request and change the header
                    current_session.headers["User-Agent"] = self.r_agent.random_agent('desktop','windows')
                    current_session.pause()
                    return self.make_request(url, method, headers, data)
                if _response.status_code == 407:
                    # Proxy authentication error, stop bot
                    raise SystemExit
                    return None
        #     time.sleep(2)
        # except Exception as e:
        #     print("\n\n\n\n\n\n\n")
        #     print("Timeout Exception Occured")
        #     print(current_session.proxies, url, e)
        #     print("\n\n\n\n\n\n\n")
        #     return self.make_request(url, method, headers, data)
        except ConnectionError as ce:
            if (isinstance(ce.args[0], MaxRetryError) and isinstance(ce.args[0].reason, ProxyError)):
                print("Could not connect to Proxy, removing the current session")    
                self.sessions.remove(current_session) 
            return _response
        #
        except Exception as e:
            print("\n\n\n\n\n\n\n")
            print("Errror occured")
            print(current_session.proxies, url, e)
            print("\n\n\n\n\n\n\n")
            if not request_error:
                print("Retrying request")
                return self.make_request(url, method, headers, data, request_error=True)
            # raise SystemExit
        del([current_session, url, method, headers, data])
        return _response