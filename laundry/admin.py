from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LaundryItem, LaundryRequest, LaundryRequestItem

admin.site.register(LaundryItem)
admin.site.register(LaundryRequest)
admin.site.register(LaundryRequestItem)
