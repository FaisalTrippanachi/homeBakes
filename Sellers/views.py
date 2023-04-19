from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'Sellers/dashboard.html')

def add_product(request):
    return render(request, 'Sellers/add_product.html')

def product_catalogue(request):
    return render(request, 'Sellers/catalogue.html')

def new_orders(request):
    return render(request, 'Sellers/new_orders.html')

def pending_orders(request):
    return render(request, 'Sellers/pending_orders.html')

def order_history(request):
    return render(request, 'Sellers/order_history.html')

def order_detail(request):
    return render(request, 'Sellers/order_detail.html')