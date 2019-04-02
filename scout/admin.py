from django.contrib import admin

# Register your models here.

from scout import models

admin.site.register(models.File)
admin.site.register(models.Job)
admin.site.register(models.Message)
admin.site.register(models.Product)
admin.site.register(models.Keyword)
admin.site.register(models.Proxy)
admin.site.register(models.User)