from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request,'HomeBake/home.html')

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