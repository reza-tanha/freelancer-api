from django.contrib import admin
from apps.advertisement.models import *


@admin.register(ADVTypes)
class ADVTypesAdmin(admin.ModelAdmin):    
    list_display = ("id", "name", "coin", "price")
    list_editable = ("coin",)
    
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):    
    list_display = ("id", "user", "status", "warning_tag")
    list_editable = ("status", "warning_tag")
    
