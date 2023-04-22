from django.shortcuts import render,redirect
from HomeBake.models import Product
from django.core.paginator import Paginator
from HomeBake.models import Cart,Seller
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
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


def change_product_status(request,id):
    product = Product.objects.get(id = id)
    product.status = 'out of stock'
    product.save()
    return redirect('seller:product_catalogue')

def product_catalogue(request):
    products = Product.objects.filter(seller = request.session['seller']).values('id','product_name','price','image','status')
    p = Paginator(products, 5) 
    page_number = request.GET.get('page')
    product_obj = p.get_page(page_number)

    return render(request, 'Sellers/catalogue.html',{'products': product_obj})

def new_orders(request):
    order_list = Cart.objects.filter(status = 'order placed',product__seller = request.session['seller'])
    print(order_list)

    p = Paginator(order_list, 2) 
    page_number = request.GET.get('page')
    order_obj = p.get_page(page_number)
    return render(request, 'Sellers/new_orders.html',{'orders': order_obj})

def pending_orders(request):
    order_list = Cart.objects.filter(status = 'in progress',product__seller = request.session['seller'])
    print(order_list)

    p = Paginator(order_list, 2) 
    page_number = request.GET.get('page')
    order_obj = p.get_page(page_number)
    return render(request, 'Sellers/pending_orders.html',{'orders': order_obj})

def order_list(request, status):
    if status == 1:
        title = 'Recent Orders'
        print('1 here')
        order_list = Cart.objects.filter(status = 'order placed',product__seller = request.session['seller'])
    
    elif status == 2:
        title = 'Pending Orders'
        print('2 here')
        order_list = Cart.objects.filter(status = 'in progress',product__seller = request.session['seller'])

    else:
        title = 'Order History'
        print('3 here')
        order_list = Cart.objects.filter(status = 'out for delivery',product__seller = request.session['seller'])

    p = Paginator(order_list, 2) 
    page_number = request.GET.get('page')
    order_obj = p.get_page(page_number)
    return render(request, 'Sellers/order_list.html',{'orders': order_obj,'title': title, 'status': status})

def order_history(request):
    order_list = Cart.objects.filter(status = 'completed',product__seller = request.session['seller'])
    print(order_list)

    p = Paginator(order_list, 2) 
    page_number = request.GET.get('page')
    order_obj = p.get_page(page_number)
    return render(request, 'Sellers/order_history.html')

def order_detail(request):
    return render(request, 'Sellers/order_detail.html')

def sales_report(request):
    return render(request, 'Sellers/sales_report.html')

def update_work_status(request,status,id):
    if status == 'in progress':
        status_code = 1
    if status == 'out for delivery':
        status_code = 2
        cart = Cart.objects.get(id = id)
        message = 'Item with Order No ' + str(cart.order_no) +' has been dispatched.'
                    

        send_mail(
                subject = 'Order Dispatch',
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [cart.customer.email]
            ) 
    Cart.objects.filter(id = id).update(status = status)
    return redirect('seller:order_list', status_code)


def logout(request):
    del request.session['seller']
    request.session.flush()
    return redirect('home_bake:customer_home')

def change_password(request):
    status_msg = ''
    if request.method  == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        try:
            if len(new_password) > 8:
                if new_password == confirm_password:
                    seller = Seller.objects.get(id = request.session['seller'])
                    if seller.password == old_password:
                        seller.password = new_password
                        seller.save()
                        status_msg = 'Password Changed'

                    else:
                        status_msg = 'Password Incorrect'
                else:
                    status_msg = 'Password Does Not Match'
            else:
                status_msg = 'Password Should Be Minimum 8 Characters'


        except:
            status_msg = 'old pss not match'
    return render(request, 'Sellers/change_password.html', {'msg': status_msg})