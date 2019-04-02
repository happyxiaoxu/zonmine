import os
import django
import io
import datetime
import requests

from django.http import HttpResponse
from django.template.loader import get_template

os.environ['DJANGO_SETTINGS_MODULE'] = 'Azondrop.settings'
django.setup()

from scout.Miner import excel
from scout.models import Job, Product, Proxy, User, File, Message

class DbHandler(object):
    def __init__(self):
        return None
    #
    def download_file(self, user, bot_name):
        # date = datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%y')
        # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename=results {}.xlsx'.format(date)
        buffer = io.BytesIO()
        workbook = excel.init_excel(bot_name=bot_name)
        sheet = workbook.active
        job = self.get_job(user)
        job_id = str(job.job_id)
        # products = Product.objects.filter(job=job).values()
        if bot_name == "search":
            products = user.job.keyword_set.filter(job_id=user.job.id).values()
            # products = Product.objects.filter(ebay_url="").values()
            files = self.get_files(job_id, "search")
            if not files:
                file = File()
                file.job_id = job_id
                file.search_file = True
                file.scout_file = False
                file.save()
            else:
                file = files[0]
        elif bot_name == "scout":
            products = user.job.product_set.filter(job_id=user.job.id).values()
            # products = Product.objects.filter(ebay_url="").values()
            files = self.get_files(job_id, "scout")
            if not files:
                file = File()
                file.job_id = job_id
                file.search_file = False
                file.scout_file = True
                file.save()
            else:
                file = files[0]

        # print(products.count())
        # print("\n\n\n\n\n\n\n")
        print(len(products))

        # print(len(products))
        # print("\n\n\n\n\n\n\n")

        max_col = sheet.max_column
        for each_product in products.iterator():
            min_row = sheet.max_row + 1
            max_row = sheet.max_row + 1
            if min_row % 507 == 0:
                print("\n\nVOILA")
                print(min_row)
            for row in sheet.iter_rows(min_row=min_row, max_col=max_col, max_row=max_row):
                for cell in row:
                    # print(cell.col_idx)
                    # print(min_row, max_row, max_col)
                    # print(excel.search_column_headers[cell.col_idx-1])
                    if bot_name == "search":
                        col_header = excel.search_column_headers[cell.col_idx - 1]
                        cell.value = each_product.get(col_header)
                        print(cell.value)

                    elif bot_name == "scout":
                        col_header = excel.scout_column_headers[cell.col_idx - 1]
                        cell.value = each_product.get(col_header)

        print("\n\nLOOP DONE SAVING TO BUFFER\n\n")
        workbook.save(buffer)
        # workbook.save(response)
        # job.refresh_from_db()
        file.refresh_from_db()
        file.file = buffer.getvalue()
        file.save()
        del [buffer,workbook]
        return None
    #
    def create_job(self, user, keywords=None, keylist=None):
        job_obj = Job(user=user, keywords=keywords, keylist=keylist)
        job_obj.save()
        return job_obj
    #
    def get_job(self, user):
        job_objs = Job.objects.filter(user=user)
        if job_objs:
            return job_objs[0]
        return None
    #
    def get_job_by_id(self, job_id):
        job_objs = Job.objects.filter(job_id=job_id)
        if job_objs:
            return job_objs[0]
        return None
    #
    def get_files(self, job_id, bot_name):
        if bot_name == "search":
            file_objs = list(File.objects.filter(job_id=job_id, search_file=True).order_by('-pk'))
            print(file_objs)
        elif bot_name == "scout":
            file_objs = list(File.objects.filter(job_id=job_id, scout_file=True).order_by('-pk'))
        else:
            file_objs = []
        # if file_objs:
        #     return file_objs[0]
        # return None        
        return file_objs
    #
    def get_proxies(self):
        proxy_objs = Proxy.objects.all()
        return proxy_objs
    #
    def create_user(self, email, password, first_name):
        new_user = User.objects.create_user(username=email, password=password, first_name=first_name)
        # for some time
        new_user.subscribed = True
        new_user.save()
        self.create_job(new_user)
        return new_user
    #
    def get_user(self, email):
        user_objs = User.objects.filter(username=email)
        if user_objs:
            return user_objs[0]
        return None
    #
    def save_message(self, name, email, message):
        new_message = Message(name=name, email=email, message=message)
        new_message.save()
        subject = "Forwarded Message of {} : {}".format(name, email)
        self.send_email("support@lootlister.com", None, subject, message)
        return new_message
    #
    def change_country(self, user, country_code):
        available_cc = dict(user.countries)
        if  country_code in available_cc:
            user.country = country_code
            user.save()
        return None
    #
    def save_product(self, product_obj, job):
        p_obj = Product()
        p_obj.job = job
        p_obj.search_keyword = product_obj.search_keyword
        p_obj.search_rank = product_obj.search_rank
        p_obj.asin = product_obj.asin
        p_obj.sponsored = product_obj.sponsored
        p_obj.title = product_obj.title
        p_obj.brand = product_obj.brand
        p_obj.price = product_obj.price
        p_obj.bread_crumbs = product_obj.bread_crumbs
        p_obj.bsr = product_obj.bsr
        p_obj.bsr_category = product_obj.bsr_category
        p_obj.review_count = product_obj.review_count
        p_obj.review_score = product_obj.review_score
        p_obj.five_star_percentage = product_obj.five_star_percentage
        p_obj.four_star_percentage = product_obj.four_star_percentage
        p_obj.three_star_percentage = product_obj.three_star_percentage
        p_obj.two_star_percentage = product_obj.two_star_percentage
        p_obj.one_star_percentage = product_obj.one_star_percentage
        p_obj.sold_by = product_obj.sold_by
        p_obj.sellers_count = product_obj.sellers_count
        p_obj.url = product_obj.url
        p_obj.in_stock = product_obj.in_stock
        p_obj.item_weight = product_obj.item_weight
        p_obj.primary_image = product_obj.primary_image
        p_obj.image1 = product_obj.image1
        p_obj.image2 = product_obj.image2
        p_obj.image3 = product_obj.image3
        p_obj.image4 = product_obj.image4
        p_obj.image5 = product_obj.image5
        p_obj.image6 = product_obj.image6
        p_obj.image7 = product_obj.image7
        p_obj.description = product_obj.description
        p_obj.is_fba = product_obj.is_fba
        p_obj.is_amz = product_obj.is_amz
        p_obj.item_model_number = product_obj.item_model_number
        p_obj.manufacturer = product_obj.manufacturer
        p_obj.is_addon = product_obj.is_addon
        p_obj.is_fbm = product_obj.is_fbm
        p_obj.is_prime = product_obj.is_prime
        p_obj.item_dimensions_length = product_obj.item_dimensions_length
        p_obj.item_dimensions_width = product_obj.item_dimensions_width
        p_obj.item_dimensions_thickness = product_obj.item_dimensions_thickness
        p_obj.feature1 = product_obj.feature1
        p_obj.feature2 = product_obj.feature2
        p_obj.feature3 = product_obj.feature3
        p_obj.feature4 = product_obj.feature4
        p_obj.feature5 = product_obj.feature5
        p_obj.cpc = product_obj.cpc
        p_obj.monthly_search_volume = product_obj.monthly_search_volume
        p_obj.competition = product_obj.competition
        p_obj.save()
        p_obj.refresh_from_db()
        return None
    #
    def send_email(self, email, template_name, subject, custom_msg=None):
        print(email, template_name, subject)
        context = {"signupEmail" : email}
        if custom_msg:
            emailHtml = custom_msg
        else:
            emailTemplate = get_template(template_name)
            emailHtml = emailTemplate.render(context)
        # email_list = [email]
        email_list = list(set([email, "support@lootlister.com"]))
        print(email_list)
        mailgunAuth = ("api", "61abed09bbd5e09f5f5464de585be2e8-a4502f89-32ddca1a")
        mailgunData = {
                        "from": "Lootlister <do-not-reply@mail.lootlister.com>",
                        "to": email_list,
                        "subject": str(subject),
                        "html": emailHtml,
                        "h:Reply-To": "Lootlister Support <support@lootlister.com>"
                    }
            #
        mailgunApiUrl = "https://api.mailgun.net/v3/mail.lootlister.com/messages"
        credentialsEmail = requests.post(mailgunApiUrl, auth=mailgunAuth, data=mailgunData)
        print(credentialsEmail)
        print(credentialsEmail.text)
        return None    