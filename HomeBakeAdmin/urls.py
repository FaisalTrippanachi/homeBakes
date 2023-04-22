
from django.urls import path,include
from . import views

app_name = 'HomeBakeAdmin'
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('sellers/<str:status>',views.sellers_list,name='sellers_list'), 
    path('users/message',views.enquiry,name='users_msg'), 
    path('customer/list',views.customers_list,name='customers_list'), 
    path('change/password',views.change_password,name='change_password'), 

    path('logout',views.logout,name='logout'), 

    path('approve/<int:id>',views.approve_Sellers,name='approve_Sellers'), 

]
