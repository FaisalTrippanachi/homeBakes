
from django.urls import path,include
from . import views

app_name = 'home_bake'

urlpatterns = [
    
    
    path('',views.product,name='customer_home'),
    path('about',views.about,name='about'),
    path('customer/register',views.customer_register,name='customer_register'),
    path('seller/check-email',views.check_seller_email,name='check_seller_email'),

    path('seller/register',views.seller_register,name='seller_register'),
    path('login/<str:user_type>',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    
    path('contact',views.contact,name='contact'),
    path('password/change',views.change_password,name='change_password'),

    # path('customer/pay',views.payment,name='payment'),

    path('product/<int:id>',views.product_details,name='product_details'),
    path('cart',views.my_cart,name='cart'),
    path('account',views.my_account,name='account'),
    path('cart/remove/<int:id>',views.remove_cart,name='remove_cart'),
    path('cart/items/order',views.order_items,name='order_items'),

    path('orders',views.my_orders,name='my_orders'),
    path('payment_page',views.payment_page,name='payment_page'),
    path('thanks/', views.thanks, name='thanks'),
    # path('create-checkout-session',views.process_payment,name='create-checkout-session')
    path('create-checkout-session/', views.create_checkout_session, name='checkout'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook')
]
