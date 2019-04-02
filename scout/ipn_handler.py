from scout.db_handler import DbHandler

db_handler = DbHandler()

PAYPAL_EMAIL = "azondrop@gmail.com"


def parser(ipn_data_dic):			
    print(str(ipn_data_dic))
    print("Parsing Ipn Message")
    custom = ipn_data_dic.get("custom")
    txn_type = ipn_data_dic.get("txn_type") 
    mc_amount3 = ipn_data_dic.get("mc_amount3")	
    receiver_email = ipn_data_dic.get("receiver_email") 
    if PAYPAL_EMAIL == receiver_email:
        print("Email check passed, our email only")
        if txn_type == "subscr_signup":	
            print("New Subscription for LootLister")
            # if mc_amount3 == "47.00":
            print("Here is the signupEmail " + str(custom))
            #Adding User
            user_obj = db_handler.get_user(custom)
            if user_obj:
                user_obj.subscribed = True
                user_obj.save()
                try:
                    print("Sending email to : " + str(custom))
                    db_handler.send_email(custom, "email_payment.html", "Lootlister Payments Confirmation")
                except Exception as e:
                    print(e)
        #										
        elif txn_type == "subscr_cancel":
            print("Cancelling Subscription for Lootlister")
            print("Here is the signupEmail " + str(custom))
            #Removing User
            user_obj = db_handler.get_user(custom)
            if user_obj:
                user_obj.subscribed = False				
                user_obj.save()



# def sendMail(custom):
#     emailTemplate = get_template("signupSuccessET.html")
#     context = {
#         "signupEmail" : custom,
#     }
#     emailHtml = emailTemplate.render(context)
#     email_list = [custom, "lootlister@gmail.com"]
#     email_list = set(email_list)
#     print(email_list)
#     mailgunAuth = ("api", "key-a210026bd7bbfec1f34654efb2bc4e37")
#     mailgunData = {
#                     # "from": "FollowPro<do-not-reply@relay.followpro.co>",
#                     "from": "UnfollowPro<do-not-reply@mailer.unfollowpro.com>",
#                     # "to": [signupEmail],
#                     "to": email_list,
#                     "subject": "UnfollowPro Credentials",
#                     "html": emailHtml,
#                 }
#         #
#     mailgunApiUrl = "https://api.mailgun.net/v3/mailer.unfollowpro.com/messages"
#     credentialsEmail = requests.post(mailgunApiUrl, auth=mailgunAuth, data=mailgunData)
#     print(credentialsEmail)
#     print(credentialsEmail.text)
#     return None



# def getDict(msg):
# 	a = msg.split("&")
# 	b = [i.split("=") for i in a]
# 	dic = {}
# 	for j in b:
# 		dic[j[0]] = j[1]
# 		print(j)
# 	return dic


# msg = 'txn_type=subscr_signup&subscr_id=I-TTRP217MG0TK&last_name=Borer&residence_country=US&mc_currency=USD&item_name=5000 UNFOLLOWS + 5000 BLOCKS&amount1=0.00&business=melimg0694@gmail.com&amount3=5.00&recurring=1&verify_sign=AATf2rd9rVjFGl2pL2Qc416hwLDOAPR9RAqx7ziSOuiKLSN.GIkw1iGZ&payer_status=verified&payer_email=borersteven@gmail.com&first_name=Steven&receiver_email=melimg0694@gmail.com&payer_id=MPNAUSWFBE9JQ&reattempt=1&item_number=5KUB&subscr_date=17:27:44 Feb 16, 2018 PST&btn_id=150467168&custom=borersteven@gmail.com&charset=windows-1252&notify_version=3.8&period1=3 D&mc_amount1=0.00&period3=1 M&mc_amount3=5.00&ipn_track_id=8dca166ebc370'




