from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.db.models import Sum
import razorpay

# Create your views here.

def home(request):
    return render(request,'HomeBake/home.html')

def customer_register(request):
    if request.method == 'POST':

        customer_name = request.POST['customer_name'].lower()
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        zipcode = request.POST['zipcode']
        location = request.POST['location']

        customer = Customer(
            customer_name = customer_name,
            email = email,
            phone = phone,
            address  = address,
            password = password,
            zipcode = zipcode,
            location = location
            
        )

        customer.save()
        return render(request, 'HomeBake/customer_register.html',{'status_msg': 'Account Created'})
        

    return render(request, 'HomeBake/customer_register.html')

def seller_register(request):

    if request.method == 'POST':

        seller_name = request.POST['seller_name'].lower()
        email = request.POST['email']
        zipcode = request.POST['zipcode']

        phone = request.POST['phone']
        address = request.POST['address']
        location = request.POST['location']

        seller = Seller(
            seller_name = seller_name,
            email = email,
            phone = phone,
            address  = address,
            zipcode = zipcode,
            location = location
            
        )

        seller.save()
        status_msg = 'Account Created'
        return render(request, 'HomeBake/seller_register.html', {'msg': status_msg})

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


def check_seller_email(request):
    input_email = request.POST['email']
    email_exist = Seller.objects.filter(email = input_email).exists()
    return JsonResponse({'status': email_exist})

def login(request, user_type):

    # previous_url = request.META.get('HTTP_REFERER')
    # print(previous_url,'PREVIOUS URL')
    # if previous_url != None:
    #     request.session['product_url'] = previous_url
    # print(request.session['product_url'],'BEFORE POST SESSION VALUE')
    # print(request.META.get('HTTP_REFERER'),'edjeid') # Here
    # # print(request.session['cart_item']) # Here
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if user_type == 'customer':

             
            try:
                customer = Customer.objects.get(email = username, password = password)
                request.session['customer']= customer.id
                request.session['zipcode'] = customer.zipcode
                request.session['customer_name'] = customer.customer_name

                request.session['location'] = customer.location

                if 'product_url' in request.session:
                     
                    redirect_path = request.session['product_url']
                     
                    del request.session['product_url']
                    return redirect(redirect_path)
                return redirect('home_bake:customer_home')
            except Exception as e:
                print(e)
                msg ='invalid email or password'    
        else:
            try:
                seller = Seller.objects.get(username = username, password = password)
                request.session['seller']=seller.id
                request.session['seller_name']=seller.seller_name
                


                
                return redirect('seller:dashboard')
            except:
                msg ='invalid email or password'    
        return render(request, 'HomeBake/login.html', {'msg': msg})
        
    return render(request, 'HomeBake/login.html')

def seller_login(request):
    return render(request, 'HomeBake/seller_login.html')

def about(request):
    return render(request,'HomeBake/about.html')

def product(request):
    products = Product.objects.all().values('id','product_name','category','image','status','seller', 'price')
    return render(request,'HomeBake/product.html', {'products': products})
  
def contact(request):
    return render(request,'HomeBake/contact.html')

def product_details(request,id):
    status_msg = ''
    if request.method == 'POST':
       


        if 'customer' in request.session:
            price = request.POST['p_price']
            qty = request.POST['cart_qty']

            cart_exist = Cart.objects.filter(product = id, customer = request.session['customer']).exists()
            if not cart_exist:
                cart = Cart(customer_id = request.session['customer'],
                            price = price, qty = qty, product_id = id)
                cart.save()
                return redirect('home_bake:cart')
            else:
                status_msg = 'Item Already in Cart'
        

        else:
            request.session['product_url'] = 'http://127.0.0.1:8000/product/'+str(id)
            print(request.session['cart_item'])
            return redirect('home_bake:login','customer')

    product = Product.objects.get(id = id)
     
    return render(request,'HomeBake/product_details.html',{'product': product, 'msg': status_msg})

def my_cart(request):
    cart_items = Cart.objects.filter(customer = request.session['customer'])
    total = Cart.objects.filter(customer = request.session['customer']).aggregate(Sum('price'))
    customer = Customer.objects.get(id = request.session['customer'])
    return render(request,'HomeBake/my_cart.html',{'cart_items': cart_items,'total': total['price__sum'], 'customer': customer})

def remove_cart(request,id):
    item = Cart.objects.get(id = id)
    item.delete()
    return redirect('home_bake:cart')
def my_account(request):
    return render(request,'HomeBake/account.html')

def my_orders(request):
    return render(request,'HomeBake/my_orders.html')

def payment(request):
    if request.method == "POST":
        amount = request.POST['total']       
        notes={'shipping address':'bomalahalli,bangolre'}

        # RAZOR pay methods 
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create( # creating a new order /(amount and nots sending to razaorpay ) 
            {"amount": float(amount) * 100, "currency": "INR", "payment_capture": "1",'notes':notes}
        )
        # end

        # creating a oder in oder table (provider id taken by new order creating time / balance detail getting after pyment susses )
        
        
         
         
        return JsonResponse(payment)
