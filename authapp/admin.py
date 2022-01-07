from django.contrib import admin

# Register your models here.
from authapp.models import ShopUser
from baskets.admin import BasketAdmin
from baskets.models import Basket


@admin.register(ShopUser)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)
