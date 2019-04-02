from django.contrib import admin
from django.urls import path

from scout import views

urlpatterns = [
    path('', views.home),
    # path('dashboard/results/<bot_name>/', views.json_results),
    path('dashboard/', views.dashboard),
    path('dashboard/stats/', views.stats),
    path('dashboard/download/', views.download_wait),
    path('dashboard/<bot_name>/download/', views.download),
    path('dashboard/<bot_name>/results/', views.results),
    path('dashboard/country/<country>/', views.country),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('results/', views.results),
    path('pricing/', views.pricing),
    path('support/', views.support),
    path('thankyou/', views.thankyou),
    path('paypal_callback/lootlister__paypal__callback/', views.paypal_ipn_handler),
    path('email_signup/', views.email_signup),
    path('email_payment/', views.email_payment),
    path('terms_of_service/', views.terms_of_service),
    path('privacy_policy/', views.privacy_policy),
]
