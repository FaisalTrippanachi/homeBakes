
from django.urls import path,include
from . import views

app_name = 'seller'
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('product/add',views.add_product,name='add_product'),
    path('product/catelogue',views.product_catalogue,name='product_catalogue'),

    path('recent/orders',views.new_orders,name='new_orders'),
    path('orders/pending',views.pending_orders,name='pending_orders'),
    path('orders/history',views.order_history,name='order_history'),
    path('orders/detail',views.order_detail,name='order_detail'),
 
]
