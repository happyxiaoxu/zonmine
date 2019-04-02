import requests
import lxml.html

from config import Config
from urllib.parse import quote_plus

import warnings
warnings.filterwarnings("ignore")

#####################################################################################
# Custom method to get first element or empty element by xpath
def xpath_first(self, elm_xpath):
    elements = self.xpath(elm_xpath)
    return next(iter(elements), lxml.html.HtmlElement())

def xpath_get_text(self, elm_xpath):
    # gets the first element and trims the text
    element = self.xpath_first(elm_xpath)
    return " ".join(element.text_content().split())

lxml.html.HtmlElement.xpath_first = xpath_first
lxml.html.HtmlElement.xpath_get_text = xpath_get_text
#####################################################################################


url = "https://www.amazon.com/dp/B07F68HHNR"
keyword = "milestone blanket cloud"
url = Config.amazon_search_url.format(quote_plus(keyword))
print(url)
url = "https://www.amazon.com/dp/B075S8VPHK"


session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"

resp = session.get(url)
print(resp.text)
xml = lxml.html.fromstring(resp.content)


# 


x1 = './/span[contains(@class, "a-text-normal")]//text() | .//img[contains(@class, "s-image")]//@alt'
xml.xpath_first(x1)