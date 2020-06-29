"""FoodPanda1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from FoodApp import views
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.home,name='home'),
    path('veg-items/',views.vegItems,name='vegItems'),
    path('non-veg-items/',views.nonVegItems,name='nonVegItems'),
    path('order-items',views.orderItems,name='orderItems'),
    path('cart-items',views.cartItems,name='cartItems'),
    path('delete-item/',views.deleteItem,name='deleteItem'),
    path('checkout-form/',views.checkoutForm,name='checkoutForm'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('my_order.html/',views.myOrder,name='my_order'),
    path('cancel_order/<int:id>/',views.cancelOrder,name='cancel_order'),
    path('reset_password/',views.resetPassword,name='reset_password'),
    path('otp_for_resetPassword',views.otp_for_resetPassword,name='otp_for_resetPassword'),
    path('new_password',views.newPassword,name='new_password'),
    path('contact_form.html/',views.contact_us,name='contact_us'),
    path('about.html/',views.aboutUs,name='aboutUs'),
    path('foods.html/',views.Food,name='food'),
    path('offers.html/',views.offers,name='offers'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
