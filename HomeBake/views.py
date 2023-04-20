from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import *

# Create your views here.

def home(request):
    return render(request,'HomeBake/home.html')

def customer_register(request):
    # if request.method == 'POST':

    #     customer_name = request.POST['customer_name']
    #     email = request.POST['email']
    #     phone = request.POST['phone']
    #     address = request.POST['address']
    #     password = request.POST['password']

    #     customer = Customer(
    #         customer_name = customer_name,
    #         email = email,
    #         phone = phone,
    #         address  = address,
    #         password = password
            
    #     )

    #     customer.save()
    #     return render(request, 'HomeBake/customer_register.html',{'status_msg': 'Account Created'})
        

    return render(request, 'HomeBake/customer_register.html')

def seller_register(request):

    # if request.method == 'POST':

    #     seller_name = request.POST['seller_name']
    #     email = request.POST['email']
    #     gender = request.POST['gender']
    #     phone = request.POST['phone']
    #     address = request.POST['address']

    #     seller = Seller(
    #         seller_name = seller_name,
    #         email = email,
    #         phone = phone,
    #         gender = gender,
    #         address  = address,
             
            
    #     )

    #     seller.save()
    #     message = '''
    #             Thank you for registering, you will get a username and temporary 
    #             password once our Admin approves your Account
    #                     '''

    #     send_mail(
    #          subject = 'account creation',
    #          message = message,
    #          from_email = settings.EMAIL_HOST_USER,
    #          recipient_list = [seller.email]
    #     ) 
    return render(request, 'HomeBake/seller_register.html')

def customer_login(request):
    return render(request, 'HomeBake/customer_login.html')

def seller_login(request):
    return render(request, 'HomeBake/seller_login.html')

def about(request):
    return render(request,'HomeBake/about.html')

def product(request):
    return render(request,'HomeBake/product.html')
  
def contact(request):
    return render(request,'HomeBake/contact.html')

def product_details(request):
    return render(request,'HomeBake/product_details.html')

def my_cart(request):
    return render(request,'HomeBake/my_cart.html')

def my_account(request):
    return render(request,'HomeBake/account.html')

def my_orders(request):
    return render(request,'HomeBake/my_orders.html')