
from django.urls import path,include
from . import views

app_name = 'home_bake'

urlpatterns = [
    
    
    path('',views.product,name='product'),
    path('about',views.about,name='about'),
    path('customer/register',views.customer_register,name='customer_register'),
    path('seller/register',views.seller_register,name='seller_register'),
    path('seller/login',views.seller_login,name='seller_login'),
    path('customer/login',views.customer_login,name='customer_login'),

    path('contact',views.contact,name='contact'),
    path('product/detail',views.product_details,name='product_details'),
    path('cart',views.my_cart,name='cart'),
    path('account',views.my_account,name='account'),
    path('orders',views.my_orders,name='my_orders')
]
