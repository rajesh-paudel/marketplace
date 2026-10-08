from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Vendor

admin.site.register(User,UserAdmin)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display=("shop_name","user","is_approved","created_at")
    list_editable=("is_approved",)
    list_filter=("is_approved",)
    search_fields=("shop_name","user__email")