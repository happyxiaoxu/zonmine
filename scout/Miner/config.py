class Config(object):
    # Amazon Configurations
    # amazon_search_url = "https://www.amazon.com/s/field-keywords={}"
    amazon_search_url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    amazon_asin_url = "https://www.amazon.com/dp/{}"
    #
    amazon_search_url_UK = "https://www.amazon.co.uk/s/field-keywords={}"
    amazon_asin_url_UK = "https://www.amazon.co.uk/dp/{}"
    #
    amazon_search_url_CA = "https://www.amazon.ca/s/field-keywords={}"
    amazon_asin_url_CA = "https://www.amazon.ca/dp/{}"
    #
    amazon_search_url_DE = "https://www.amazon.de/s/field-keywords={}"
    amazon_asin_url_DE = "https://www.amazon.de/dp/{}"
    #
    amazon_search_url_FR = "https://www.amazon.fr/s/field-keywords={}"
    amazon_asin_url_FR = "https://www.amazon.fr/dp/{}"
    #
    gw_api_key = "72053e406150c3f"
    gw_api_url = "http://api.grepwords.com/lookup?apikey={}&q={}".format(gw_api_key, "{}")
    # General
    requests_per_session = 500 # A new session is created with new proxy for rotation
    thread_count = 20
    # thread_count = 1
    pause_time_min = 120
    pause_time_max = 300