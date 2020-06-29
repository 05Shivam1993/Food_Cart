from django.contrib import admin
from FoodApp.models import Order,Foods,Offers

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','name','mobile','email','category','dish_name','quantity',
    'delievery_status','cost','address','date','cancel_order']

class FoodsAdmin(admin.ModelAdmin):
    list_display = ['id','item','price','category','image']

class OffersAdmin(admin.ModelAdmin):
    list_display = ['coupons','percentage','cost_applicable']

admin.site.register(Order,OrderAdmin)
admin.site.register(Foods,FoodsAdmin)
admin.site.register(Offers,OffersAdmin)
