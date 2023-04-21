from django.shortcuts import render
from HomeBake.models import Product
# Create your views here.


def dashboard(request):
    return render(request, 'Sellers/dashboard.html')

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name'].lower()
        price = request.POST['price']
        ingredients = request.POST['ingredients']
        pic = request.FILES['pic']
        category = request.POST['category']

        product_exist = Product.objects.filter(product_name = product_name, 
                                               category = category,
                                         seller = request.session['seller']).exists()
        if not product_exist:
            Product(product_name = product_name, seller_id = request.session['seller'],
                    price = price, ingredients_used = ingredients,
                      image = pic, category = category ).save()

            status_msg = 'Product Added Succesfully'
        else:
            status_msg = 'Product Name Exists'

        return render(request, 'Sellers/add_product.html', {'msg': status_msg})
            
    return render(request, 'Sellers/add_product.html')

def product_catalogue(request):
    products = Product.objects.filter(seller = request.session['seller']).values('product_name','price','image','status')
    return render(request, 'Sellers/catalogue.html',{'products': products})

def new_orders(request):
    return render(request, 'Sellers/new_orders.html')

def pending_orders(request):
    return render(request, 'Sellers/pending_orders.html')

def order_history(request):
    return render(request, 'Sellers/order_history.html')

def order_detail(request):
    return render(request, 'Sellers/order_detail.html')