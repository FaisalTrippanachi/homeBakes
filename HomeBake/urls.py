
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('about',views.about,name='about'),
    path('product',views.product,name='product'),
    path('home',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('productdetails',views.product_details,name='productdetails'),
    path('cart',views.my_cart,name='cart'),
    path('account',views.my_account,name='account'),
    path('orders',views.my_orders,name='my_orders')
]
