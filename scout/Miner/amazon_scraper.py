# from .config import Config
# from .product import Product
from scout.Miner.config import Config
from scout.Miner.product import Product
from scout.Miner.grepwords_api import KeywordsApi

import lxml.html
import re

# from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
from urllib.parse import quote_plus
from collections import OrderedDict

import warnings
warnings.filterwarnings("ignore")

#####################################################################################
# Custom method to get first element or empty element by xpath
def xpath_first(self, elm_xpath):
    elements = self.xpath(elm_xpath)
    empty_elm = lxml.html.HtmlElement()
    empty_elm.text = "-"
    return next(iter(elements), empty_elm)

def xpath_get_text(self, elm_xpath):
    # gets the first element and trims the text
    element = self.xpath_first(elm_xpath)
    return " ".join(element.text_content().split())

lxml.html.HtmlElement.xpath_first = xpath_first
lxml.html.HtmlElement.xpath_get_text = xpath_get_text
#####################################################################################

def check_similarity(a, b):
    i = SequenceMatcher(None, a, b)
    return i.ratio()


class AmazonScraper(object):
    def __init__(self, scraper_obj):
        # Scraper.__init__(self)
        self.scraper_obj = scraper_obj
        self.kw_api = KeywordsApi()
        return None
    #
    def asin_search(self, product_obj):
        asin = product_obj.asin
        print("ASIN : {}".format(asin))
        # https://www.amazon.com/dp/B075QDGZX9
        asin_url = Config.amazon_asin_url.format(asin)
        # asin_resp = self.session.get(asin_url)
        asin_resp = self.scraper_obj.make_request(asin_url)
        if asin_resp.status_code != 200:
            print("Skipping ASIN Search as status code is: {}".format(asin_resp.status_code))
            return product_obj
        asin_xml = lxml.html.fromstring(asin_resp.content)
        print(asin_resp)
        print(asin_resp.url)
        product_obj.asin = asin
        product_obj.url = asin_url
        # product_obj.title = asin_xml.xpath_get_text('//span[@id="productTitle"]')
        product_obj.bread_crumbs = asin_xml.xpath_get_text('//div[contains(@class, "a-breadcrumb")]')
        # brand = asin_xml.xpath_first('//a[@id="bylineInfo"] | //a[@id="brand"]').attrib.get("href")
        # if brand:
        #     product_obj.brand = brand.split("/")[1]
        product_obj.brand = asin_xml.xpath_get_text('//a[@id="bylineInfo"] | //a[@id="brand"]')
        product_obj.description = asin_xml.xpath_get_text('//div[@id="productDescription" and contains(@class, "a-section")]//p')
        # product_obj.weight = asin_xml.xpath_get_text('''
        # //th[contains(text(), "Weight")]/following-sibling::td | //text()[contains(.,'Weight')]/ancestor::li
        # ''')
        product_obj.item_model_number = asin_xml.xpath_get_text('''
        //*[contains(text(), "Item model number")]/following-sibling::td | //text()[contains(.,'Item model number')]/ancestor::li
        ''')
        # product_obj.item_dimensions = asin_xml.xpath_get_text('''
        # //th[contains(text(), "Product Dimensions")]/following-sibling::td | //th[contains(text(), "Item Dimensions")]/following-sibling::td
        # ''')
        # BSR Data
        bsr_data = asin_xml.xpath_first('''
                    //*[contains(text(), "Best Sellers Rank")]/following-sibling::td
                ''').text.strip("(").strip().split("in") + ["-", "-"]
        product_obj.bsr = bsr_data[0]
        product_obj.bsr_category = bsr_data[1]
        #
        # Dimensions, in inches
        # //th[contains(text(), "Dimensions")]/following-sibling::td | //text()[contains(.,'Dimensions')]/ancestor::li
        dimensions_text = asin_xml.xpath_get_text('''
                //*[contains(text(), "Dimensions")]/following-sibling::td | //text()[contains(.,'Dimensions')]/ancestor::li
            ''').split("inches")[0]
        dimensions = re.findall(r"[-+]?\d*\.\d+|\d+", dimensions_text)
        if dimensions:
            dimensions = [float(i) for i in sorted(dimensions, reverse=True)]
        dimensions = (dimensions + ["-", "-", "-"])[:3]
        product_obj.item_dimensions_length = dimensions[0]
        product_obj.item_dimensions_width = dimensions[1]
        product_obj.item_dimensions_thickness = dimensions[2]
        ########
        # Item Weight, convert ounces to pounds by dividing with 16
        # Alt. Xpaths: 
        #         //th[contains(text(), "Shipping Weight")]/following-sibling::td | //th[contains(text(), "Item Weight")]/following-sibling::td
        #        //*[contains(text(), "Item Weight")]/following-sibling::td | //*[contains(text(), "Shipping Weight")]/following-sibling::td
        item_weight_text = asin_xml.xpath_get_text('''
                //*[contains(text(), "Weight")]/following-sibling::td
            ''')
        item_weight = re.search(r"[-+]?\d*\.\d+|\d+", item_weight_text)
        if item_weight:
            item_weight = item_weight.group()
            if "ounce" in item_weight_text:
                print("Converting ounce to pound")
                item_weight = float(item_weight) / 16
            product_obj.item_weight = item_weight
        # Fullfillment
        # print(result.xpath_first('.//span[contains(@class, "s-sponsored-info-icon")]').tag)
        if asin_xml.xpath('//text()[contains(., "sold by Amazon")]'):
            product_obj.is_amz = True 
        elif asin_xml.xpath('//text()[contains(., "Fulfilled by Amazon")]'):
            product_obj.is_fba = True   
        else:
            product_obj.is_fbm = True   
        ############################
        # /html/body//text()[matches(.,'test', 'i')]
        product_obj.manufacturer = asin_xml.xpath_get_text('//th[contains(text(), "Manufacturer")]/following-sibling::td')
        # product_obj.sold_by = asin_xml.xpath_get_text('//div[@id="merchant-info"]//a[1] | //div[@id="merchant-info"]')
        # product_obj.sold_by = asin_xml.xpath_get_text('//*[@id="merchant-info"]//a[1] | //*[@id="merchant-info"]')
        product_obj.sold_by = asin_xml.xpath_get_text('//*[@id="merchant-info"]//a')
        # product_obj.in_stock = asin_xml.xpath_get_text('//div[@id="availability"]')
        product_obj.in_stock = asin_xml.xpath_get_text('//*[@id="availability"]')
        # Extracting Features
        features_elm = asin_xml.xpath('//div[@id="feature-bullets"]//li//span[not(descendant:: a) and contains(@class, "a-list-item")]/text()') #not complete
        features = [" ".join(each_feature.split()) for each_feature in features_elm] + ["-", "-", "-", "-", "-"]
        features = features[:5]
        product_obj.feature1 = features[0]
        product_obj.feature2 = features[1]
        product_obj.feature3 = features[2]
        product_obj.feature4 = features[3]
        product_obj.feature5 = features[4]
        #####
        sellers_count = re.search(r'\((.*?)\)', asin_xml.xpath_first('//div[@id="olp_feature_div"]').text_content())
        if sellers_count:
            product_obj.sellers_count = sellers_count.group(1)
        print(product_obj.sellers_count)
        #Extracting Images
        # images_elm = asin_xml.xpath_first('//script[contains(text(), "ImageBlockATF") and not(contains(text(), "imageBlockATF"))]')[0]
        thumb_images = asin_xml.xpath('//li[contains(@class,"item")]//span[contains(@class,"a-button-thumbnail")]//img/@src')
        images = [re.sub(pattern = r'_.+_.', string=img, repl = "") for img in thumb_images] + ["-", "-", "-", "-", "-", "-", "-", "-"]
        images = images[:7]
        product_obj.image1 = images[0]
        product_obj.image2 = images[1]
        product_obj.image3 = images[2]
        product_obj.image4 = images[3]
        product_obj.image5 = images[4]
        product_obj.image6 = images[5]
        product_obj.image7 = images[6]
        # product_obj.image_8 = images[7]
        # Review Percentage
        product_obj.five_star_percentage = asin_xml.xpath_get_text('//a[contains(@class, "5star histogram-review-count")]')
        product_obj.four_star_percentage = asin_xml.xpath_get_text('//a[contains(@class, "4star histogram-review-count")]')
        product_obj.three_star_percentage = asin_xml.xpath_get_text('//a[contains(@class, "3star histogram-review-count")]')
        product_obj.two_star_percentage = asin_xml.xpath_get_text('//a[contains(@class, "2star histogram-review-count")]')
        product_obj.one_star_percentage = asin_xml.xpath_get_text('//a[contains(@class, "1star histogram-review-count")]')
        del([asin, asin_url, asin_resp, asin_xml, features_elm, thumb_images, images])
        return product_obj
    #
    def keyword_search(self, keyword,job,db_handler):
        job.refresh_from_db()
        # print("Searching Amazon")
        products = []
        print(keyword)
        print(quote_plus(keyword))
        print("Current Keyword {}".format(keyword))
        search_url = Config.amazon_search_url.format(quote_plus(keyword))
        print(search_url)
        search_resp = self.scraper_obj.make_request(search_url)
        print(search_resp)
        print(search_resp.url)
        if search_resp.status_code != 200:
            print("Skipping keywords as status code is: {}".format(search_resp.status_code))
            return products
        search_xml = lxml.html.fromstring(search_resp.content)
        print(search_xml)
        print('///////////////////')
        kw_stats = self.kw_api.get_stats([keyword])
        cpc = kw_stats[keyword][0]
        monthly_search_volume = kw_stats[keyword][1]
        competition = kw_stats[keyword][2]
        #  Edit xpath to include sponsored listings
        # search_results = search_xml.xpath('//div[@id="resultsCol"]//li[not(.//h5) and contains(@class, "s-result-item")]')
        # search_results = search_xml.xpath('//div[contains(@class, "s-result-list")]//div[@data-asin]')[:1]
        search_results = search_xml.xpath('//div[contains(@class, "s-result-list")]//div[@data-asin]')
        # search_results_1 = search_xml.xpath('//div[@id="resultsCol"]//li[@data-asin]//h2')
        # search_results = search_xml.xpath('//div[contains(@class, "s-result-list")]//div[@data-asin]')
        print(len(search_results))
        # if not search_results:
        #     with open("test.html", "wb") as oo:
        #         oo.write(search_resp.content)
        if not search_results:
            print("No results found for keyword : {}".format(keyword))
            return products
        for result in search_results:
            product_obj = Product()
            url = result.xpath('.//span[contains(@class, "a-text-normal")]/parent::a/@href')
            title = result.xpath_first('.//span[contains(@class, "a-text-normal")]//text() | .//img[contains(@class, "s-image")]//@alt')
            print(title.encode())
            asin = result.attrib.get("data-asin")
            price = result.xpath_get_text('.//span[@class="a-offscreen"]')
            primary_image = result.xpath_first('.//img[@srcset and @data-image-load]/@src')
            review_count = result.xpath_first('.//a[contains(@href, "customerReviews")]').text_content().strip()
            review_score = result.xpath_first('.//i[contains(@class,"a-icon-star")]//span').text_content().split(" ")[0]
            is_prime = False
            is_addon = False
            is_sponsored = False
            # print(result.xpath_first('.//span[contains(@class, "s-sponsored-info-icon")]').tag)
            if result.xpath('.//i[contains(@class,"a-icon-prime")]'):
                is_prime = True   
            if result.xpath('.//i[contains(@class,"a-icon-addon")]'):
                is_addon = True   
            if result.xpath('.//div[@data-component-type="sp-sponsored-result"]'):
                print("Inside is sponsored")
                is_sponsored = True   
            #Updating Counter to rotate proxies
            # Get details from ASIN
            # self.update_counter()
            product_obj.search_keyword              = keyword
            product_obj.search_rank                 = search_results.index(result) + 1
            product_obj.url                         = url
            product_obj.asin                        = asin
            product_obj.title                       = title
            product_obj.price                       = price
            product_obj.primary_image               = primary_image
            product_obj.review_count                = review_count
            product_obj.review_score                = review_score
            product_obj.is_prime                    = is_prime
            product_obj.is_addon                    = is_addon
            product_obj.sponsored                = is_sponsored
            product_obj.cpc                         = cpc
            product_obj.monthly_search_volume       = monthly_search_volume
            product_obj.competition                 = competition
            print(is_sponsored)
            # products.append(product_obj)
            products.append(self.asin_search(product_obj))
            db_handler.save_product(product_obj,job)
            job.scout_results_counter += 1
            job.save()
            job.refresh_from_db()
            del([product_obj])
            # break
        # with open("test.html", "wb") as oo:
        #     oo.write(search_resp.content)
        return products