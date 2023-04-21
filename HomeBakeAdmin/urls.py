
from django.urls import path,include
from . import views

app_name = 'HomeBakeAdmin'
urlpatterns = [
    
    path('',views.dashboard,name='dashboard'),
    path('sellers/<str:status>',views.sellers_list,name='sellers_list'), 
    path('approve/<int:id>',views.approve_Sellers,name='approve_Sellers'), 

]
