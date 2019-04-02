from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

import django.contrib.auth as djangoAuth
from django.views.decorators.csrf import csrf_exempt

import threading
import datetime
import requests

from rq import Queue
from collections import OrderedDict
from scout.worker import conn

# from scout.Code import scraper
# from scout.Code import ebay_scraper
# from scout.Code import amazon_scraper
# from scout import db_handler
from scout.db_handler import DbHandler
from scout import ipn_handler

db_handler = DbHandler()

from scout.utils import start_search, start_scout

# scraper_obj = scraper.Scraper()
# es_obj = ebay_scraper.EbayScraper(scraper_obj)
# as_obj = amazon_scraper.AmazonScraper(scraper_obj)

q = Queue(connection=conn, default_timeout=1800)


def ipn_parser(request):
	##################################################################################
	###############VERIFYNG AND ACKNOWLDEGING IPN'S MESSAGE, NO MATTER WHAT###########
	print("Inside the thread!!")
	print("\n\n\n\nin view ipn_handler\n\n\n\n")
	print(list(request.POST.items()))
	# print(request.POST.getlist('ids[]'))
	# print((request.POST.urlencode))
	ipn_data_dic = request.POST.dict()
	print(ipn_data_dic)
	print((request.POST.urlencode()))
	# print(dir(request.POST))
	ipn_data = "cmd=_notify-validate&" + request.POST.urlencode()
	print(ipn_data)
	####Empty 200 request sent to paypal
	# requests.post("https://ipnpb.sandbox.paypal.com/cgi-bin/webscr")
	requests.post("https://www.paypal.com/cgi-bin/webscr")
	#####Sending back the same data to paypal
	# d = requests.post("https://ipnpb.sandbox.paypal.com/cgi-bin/webscr", data = ipn_data)
	d = requests.post("https://www.paypal.com/cgi-bin/webscr", data = ipn_data)
	print(d)
	print(d.text.encode())
	######################################################################################
	#ipn_data_dic,d
	if d.text == "VERIFIED":
		print("Saved logs")
		if ipn_data_dic.get("test_ipn") == None:
			print("Real Message")
			ipn_handler.parser(ipn_data_dic)
		else:
			print("Test Message")
			# ipn_handler.parser(ipn_data_dic)	
	return None

@csrf_exempt
def paypal_ipn_handler(request):
	if request.method == "POST":
		# ipn_parser_thread_obj = threading.Thread(target=lambda : ipn_parser(request))
		# ipn_parser_thread_obj.start()
		ipn_parser(request)
		return HttpResponse("")

def home(request):
    return render(request, "home.html", context={})

def terms_of_service(request):
    return render(request, "terms_of_service.html", context={})

def privacy_policy(request):
    return render(request, "privacy_policy.html", context={})

def thankyou(request):
    return render(request, "thankyou.html", context={})

def email_signup(request):
    return render(request, "email_signup.html", context={})

def email_payment(request):
    return render(request, "email_payment.html", context={})

def results(request, bot_name):
    if request.user.is_authenticated:
        if request.method == "GET":
            if bot_name == "search":
                # results = request.user.job.product_set.exclude(ebay_url="").order_by("-id")[:100]
                results = request.user.job.keyword_set.filter(job_id=request.user.job.id).order_by("keyword")[:100]
                context = {"results": results}
                return render(request, "search_results.html", context=context)
            elif bot_name == "scout":
                results = request.user.job.product_set.filter(job_id=request.user.job.id)[:100]
                context = {"results": results}
                return render(request, "scout_results.html", context=context)
    return HttpResponse(status=400)

def download_wait(request):
    bot_name = request.session["bot_name"]
    print('bot name:{}'.format(bot_name))
    return render(request, "download.html", context={"bot_name": bot_name})

def download(request, bot_name):
    if request.user.is_authenticated:
        request.session["bot_name"] = bot_name
        job_obj = request.user.job
        job_id = str(job_obj.job_id)
        #
        if request.method == "POST":
            files = db_handler.get_files(job_id, bot_name)
            print("\n\n These are files in post requests")
            print(files)
            if files:
                file = files[0]
                file.file = None
                file.save()
                file.refresh_from_db()
                del ([file])
            #
            print("Starting download thread")
            file_download_thread = threading.Thread(target=lambda:db_handler.download_file(request.user, bot_name))
            file_download_thread.start()
            file_download_thread.join()

            del ([file_download_thread,job_obj,job_id,files])
            print("Download thread started", bot_name)
            # response = db_handler.download_file(request.user, bot_name)
            return redirect("/dashboard/download/")
        #
        elif request.method == "GET":
            date = datetime.datetime.strftime(datetime.datetime.now(), '%m-%d-%y') 
            if bot_name == "search":
                print("Inside Search File")
                search_files = db_handler.get_files(job_id, bot_name)
                if search_files:
                    search_file = search_files[0].file
                    if search_file:
                        print("Giving Search File")
                        response = HttpResponse(
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        response['Content-Disposition'] = 'attachment; filename=search_results {}.xlsx'.format(date)
                        response.write(search_file)
                        return response
                    return HttpResponse(status=200)
            #
            elif bot_name == "scout":
                print("Inside Scout File")
                scout_files = db_handler.get_files(job_id, bot_name)

                if scout_files:
                    scout_file = scout_files[0].file
                    if scout_file:
                        print("Giving Scout File")
                        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        response['Content-Disposition'] = 'attachment; filename=scout_results {}.xlsx'.format(date)
                        response.write(scout_file)
                        return response
                    return HttpResponse(status=200)
        return redirect("/dashboard/")
    return redirect("/")

def stats(request):
    if request.user.is_authenticated:
        results = {
            "search_status": request.user.job.search_results_counter,
            "search_stats": request.user.job.search_status,
            "scout_status": request.user.job.scout_results_counter,
            "scout_stats": request.user.job.scout_status,
        }
        return JsonResponse(results)
    return redirect("/")
#
def pricing(request):
    return render(request, "pricing.html")
#
def support(request):
    if request.method == "GET":
        return render(request, "support.html")
    elif request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")        
        # Create Message
        message_obj = db_handler.save_message(name, email, message)
        message_obj.save()        
        return HttpResponse(status=200)
    return HttpResponse(status=400)
#
def country(request, country):
    if request.user.is_authenticated:
        print(country)
        db_handler.change_country(request.user, country)
        return redirect("/dashboard/")
    return redirect("/")
#
def dashboard(request):
    if request.user.is_authenticated:
        job_obj = request.user.job
        job_id = str(job_obj.job_id)
        if request.method == "POST":
            action = request.POST.get("action")
            name = request.POST.get("name")
            print("In dashboard")
            print(action)
            if action == "start":         
                # job_obj.product_set.all().delete()  # Delete all products
                if name == "search":
                    job_obj.keyword_set.exclude(keyword="").delete()  # Delete all products
                    print("Starting Search")
                    keywords = request.POST.get('keywords')
                    [file.delete() for file in db_handler.get_files(job_id, "search")]
                    # job_obj.search_file = None
                    job_obj.keywords = keywords
                    job_obj.search_status = True
                    job_obj.save()
                    # q.enqueue(start_scout, job_id, result_ttl=0)
                    start_search(job_id)
                    # print(q.get_jobs())
                    # q.enqueue(start_scout, job_obj, es_obj, as_obj)
                    # start_scout(job_obj, es_obj, as_obj)
                elif name == "scout":
                    print("Starting Scout")
                    job_obj.product_set.all().delete()  # Delete all products
                    keylist = request.POST.get('keylist')
                    [file.delete() for file in db_handler.get_files(job_id, "scout")]
                    # job_obj.scout_file = None
                    job_obj.keylist = keylist
                    job_obj.scout_status = True
                    job_obj.save()
                    # q.enqueue(start_asin, job_id, result_ttl=0)
                    start_scout(job_id)
                    # print(q.get_jobs())
                    # start_asin(job_obj)
            #
            elif action == "stop":
                if name == "search":
                    print("Stopping Search")
                    job_obj.search_status = False
                    job_obj.save()
                elif name == "scout":
                    print("Stopping Scout")
                    job_obj.scout_status = False
                    job_obj.save()    
            return HttpResponse(status=200)
        else:
            context={
                "job": job_obj
            }
            print(job_obj)
            print('//////////')
            if request.user.subscribed:
                return render(request, "dashboard.html", context=context)
            else:
                return render(request, "select_package.html", context=context)

    return render(request, "login_error.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    else:
        if request.method == "POST":
            print(request.user.is_authenticated)
            print("Logging In")
            loginEmail = request.POST['email']
            loginPassword = request.POST['password']
            print(loginEmail, loginPassword)
            user = djangoAuth.authenticate(request, username=loginEmail, password=loginPassword)
            if user is not None:
                djangoAuth.login(request, user)
                print("Logged In")
                # return JsonResponse({"status":"success", "message": "Login Successfull"})
                return redirect("/dashboard/")
            else:
                return JsonResponse({"status":"error", "message":"Email / Password incorrect"})
    return redirect("/")
#	
def logout(request):
    djangoAuth.logout(request)
    return redirect("/")
#
def register(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")		
    else:
        if request.method == "POST":
            print("new user")
            print(request.POST)
            registrationEmail = request.POST['email']
            registrationPassword = request.POST['password']
            registrationName = request.POST['name']
            print(registrationName, registrationEmail, registrationPassword)
            # return JsonResponse({"status":"error", "message":"{} is already registered".format(registrationEmail)})
            db_handler.create_user(registrationEmail, registrationPassword, registrationName)
            user = djangoAuth.authenticate(request, username=registrationEmail, password=registrationPassword)
            if user:
                djangoAuth.login(request, user)
                email_thread = threading.Thread(target=lambda: db_handler.send_email(registrationEmail, "email_signup.html", "Lootlister Registration Successful"))
                email_thread.start()
                # return redirect("/dashboard/")
                # return JsonResponse({"status":"success"})
                return redirect("/dashboard/")
            # return JsonResponse({'status':'success','message':'Signed Up Successfully', 'registrationEmail' : registrationEmail})	
    return redirect("/")
