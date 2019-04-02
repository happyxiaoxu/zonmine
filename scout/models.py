from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

class User(AbstractUser):
    # countries = (
    #                 ("CA", "Canada"),
    #                 ("IT", "Italy"),
    #                 ("SP", "Spain"),
    #                 ("UK", "United Kingdom"),
    #                 ("USA", "United States"),
    #             ) 
    countries = (
                    ("CA", "Canada"),
                    ("DE", "Germany"),
                    ("FR", "France"),
                    ("GB", "United Kingdom"),
                    ("US", "United States"),
                ) 
    subscribed = models.BooleanField("Subscribed", default=False)
    country = models.CharField("Country", max_length=20, default="US", choices=countries)  

class Proxy(models.Model):
	class Meta:
		verbose_name_plural = "Proxies"

	def __str__(self):
		return self.ip

	ip = models.CharField("Proxy Ip", blank=True, null=True, default=None, max_length=200) 


class Message(models.Model):
    def __str__(self):
        return self.name + " : " + self.email

    name = models.CharField("Name", max_length = 200, default=None, blank=True, null=True)
    email = models.CharField("Email", max_length = 200, default=None, blank=True, null=True)
    message = models.TextField("Message", max_length = 2000, default=None, blank=True, null=True)



class File(models.Model):
    file = models.BinaryField("File", default=None, blank=True, null=True)
    search_file = models.BooleanField("Search File", default=False)
    scout_file = models.BooleanField("Scout File", default=False)
    job_id = models.CharField("Job Id", max_length=200, default=None, blank=True, null=True)

class Job(models.Model):
    def __str__(self):
        return self.user.username + " : " + str(self.job_id)
    #    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    keywords = models.TextField("Keywords", max_length = 20000, default=None, blank=True, null=True)
    keylist = models.TextField("Key List", max_length = 20000, default=None, blank=True, null=True)
    # scout_file = models.BinaryField("Scout File", default=None, blank=True, null=True)
    # asin_file = models.BinaryField("ASIN File", default=None, blank=True, null=True)
    search_status = models.BooleanField("Search Status", default=False)
    scout_status = models.BooleanField("Scout Status", default=False)
    search_results_counter = models.IntegerField("Search Results Count", default=0, blank=True, null=True)
    scout_results_counter = models.IntegerField("Scout Results Count", default=0, blank=True, null=True)

class Product(models.Model):
    def __str__(self):
        return self.job.user.username + " : " + str(self.job.job_id) + "Scout: "

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    search_keyword = models.CharField("Search Keyword", max_length = 2000, default=None, blank=True, null=True)
    search_rank = models.IntegerField("Search Rank", default=0,blank=True, null=True)
    asin = models.CharField("ASIN", max_length = 2000, default=None, blank=True, null=True)
    sponsored = models.BooleanField("Is Sponsored", default=False)
    title = models.CharField("Title", max_length = 2000, default=None, blank=True, null=True)
    brand = models.CharField("Brand", max_length = 2000, default=None, blank=True, null=True)
    price = models.CharField("Price", max_length = 2000, default=None, blank=True, null=True)
    bread_crumbs = models.CharField("Bread Crumbs", max_length = 2000, default=None, blank=True, null=True)
    bsr = models.CharField("BSR", max_length = 2000, default=None, blank=True, null=True)
    bsr_category = models.CharField("BSR Category", max_length = 2000, default=None, blank=True, null=True)
    review_count = models.CharField("Review Count", max_length = 2000, default=None, blank=True, null=True)
    review_score = models.CharField("Review Score", max_length = 2000, default=None, blank=True, null=True)
    five_star_percentage = models.CharField("Five Star Percentage", max_length = 2000, default=None, blank=True, null=True)
    four_star_percentage = models.CharField("Four Star Percentage", max_length = 2000, default=None, blank=True, null=True)
    three_star_percentage = models.CharField("Three Star Percentage", max_length = 2000, default=None, blank=True, null=True)
    two_star_percentage = models.CharField("Two Star Percentage", max_length = 2000, default=None, blank=True, null=True)
    one_star_percentage = models.CharField("One Star Percentage", max_length = 2000, default=None, blank=True, null=True)
    sold_by = models.CharField("Sold By", max_length = 2000, default=None, blank=True, null=True)
    sellers_count = models.CharField("Sellers Count", max_length = 2000, default=None, blank=True, null=True)
    url = models.CharField("URL", max_length = 2000, default=None, blank=True, null=True)
    in_stock = models.CharField("In Stock", max_length = 2000, default=None, blank=True, null=True)
    item_weight = models.CharField("Item Weight", max_length = 2000, default=None, blank=True, null=True)
    primary_image = models.CharField("Primary Image", max_length = 2000, default=None, blank=True, null=True)
    image1 = models.CharField("Image 1", max_length = 2000, default=None, blank=True, null=True)
    image2 = models.CharField("Image 2", max_length = 2000, default=None, blank=True, null=True)
    image3 = models.CharField("Image 3", max_length = 2000, default=None, blank=True, null=True)
    image4 = models.CharField("Image 4", max_length = 2000, default=None, blank=True, null=True)
    image5 = models.CharField("Image 5", max_length = 2000, default=None, blank=True, null=True)
    image6 = models.CharField("Image 6", max_length = 2000, default=None, blank=True, null=True)
    image7 = models.CharField("Image 7", max_length = 2000, default=None, blank=True, null=True)
    description = models.CharField("Description", max_length = 2000, default=None, blank=True, null=True)
    is_fba = models.BooleanField("Is FBA", default=False)
    is_amz = models.BooleanField("Is AMZ", default=False)
    item_model_number = models.CharField("Item Model Number", max_length = 2000, default=None, blank=True, null=True)
    manufacturer = models.CharField("Manufacturer", max_length = 2000, default=None, blank=True, null=True)
    is_addon = models.BooleanField("Is Addon", default=False)
    is_fbm = models.BooleanField("Is FBM", default=False)
    is_prime = models.BooleanField("Is Prime", default=False)
    item_dimensions_length = models.TextField("Item Dimensions Length", max_length = 2000, default=None, blank=True, null=True)
    item_dimensions_width = models.TextField("Item Dimensions Width", max_length = 2000, default=None, blank=True, null=True)
    item_dimensions_thickness = models.TextField("Item Dimensions Thickness", max_length = 2000, default=None, blank=True, null=True)
    feature1 = models.TextField("Feature 1", max_length = 3000, default=None, blank=True, null=True)
    feature2 = models.TextField("Feature 2", max_length = 3000, default=None, blank=True, null=True)
    feature3 = models.TextField("Feature 3", max_length = 3000, default=None, blank=True, null=True)
    feature4 = models.TextField("Feature 4", max_length = 3000, default=None, blank=True, null=True)
    feature5 = models.TextField("Feature 5", max_length = 3000, default=None, blank=True, null=True)
    cpc = models.TextField("CPC", max_length = 3000, default=None, blank=True, null=True)
    monthly_search_volume = models.CharField("Monthly Search Volume", max_length = 2000, default=None, blank=True, null=True)
    competition = models.CharField("Competition", max_length = 2000, default=None, blank=True, null=True)
    #timestamps
    updated_timestamp = models.DateTimeField("Last Updated At", auto_now=True, null=True)
    created_timestamp = models.DateTimeField("Created At", auto_now_add=True, null=True)

class Keyword(models.Model):
    def __str__(self):
        return str(self.job.job_id) + " : " + self.keyword
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    keyword = models.CharField("Keyword", max_length = 2000, default=None, blank=True, null=True)





