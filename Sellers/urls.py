
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
    path('orders/<int:status>',views.order_list,name='order_list'),

    path('update/work-status/<str:status>/<int:id>',views.update_work_status,name='update_work_status'),

    path('logout',views.logout,name='logout'),
    path('sales/report',views.sales_report,name='sales_report'),

    path('password/change',views.change_password,name='change_password'),


    

    path('product/change-status/<int:id>',views.change_product_status,name='change_product_status'),
 
]
