from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.db.models import Q
from django.db.models import Sum,F
from django.core.paginator import Paginator
from datetime import date
from datetime import datetime,timedelta
import random
import stripe
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

def home(request):
    return render(request,'HomeBake/home.html')

def payment_page(request):
    amount = 200
    return render(request, 'HomeBake/payment.html', {'amount': amount})

def thanks(request):
    return render(request, 'thanks.html')

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
        elif user_type == 'seller':
            try:
                seller = Seller.objects.get(username = username, password = password)
                request.session['seller']=seller.id
                request.session['seller_name']=seller.seller_name
                


                
                return redirect('seller:dashboard')
            except:
                msg ='invalid email or password'    
        
        else:
            try:
                admin = Admin.objects.get(user_id = username, password = password)
                request.session['admin']= admin.id
                return redirect('HomeBakeAdmin:dashboard')
            except:
                msg ='invalid email or password'    
        return render(request, 'HomeBake/login.html', {'msg': msg})

    return render(request, 'HomeBake/login.html')

def seller_login(request):
    return render(request, 'HomeBake/seller_login.html')

def about(request):
    return render(request,'HomeBake/about.html')

def product(request):
    
    
    if request.method == 'POST':
        
        search_text = request.POST['search_text']
        if search_text != '':
            search_result = Product.objects.filter(Q(seller__zipcode = search_text) | Q(seller__location = search_text))
            
            return render(request,'HomeBake/product.html', {'products': search_result})
    
    products = Product.objects.all()
    return render(request,'HomeBake/product.html', {'products': products})
  
def contact(request):
    status_msg = ""
    # for i in range(0,20):
    #     CustomerContact(
    #         customer_name = 'test'+str(i),
    #         email = 'test@gmail.com',
    #         phone = '889988888',
    #         message = 'loreeefhuuf rfrifrf iurf eripr3f rfeffkj',
    #         date = '2023-04-22'
            
    #     ).save()


    if request.method == 'POST':

        name = request.POST['name'].lower()
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contact_date = date.today()

        contact = CustomerContact(
            customer_name = name,
            email = email,
            phone = phone,
            message = message,
            date = contact_date
            
        )

        contact.save()
        status_msg = 'Message Sent Succesfully'
    return render(request,'HomeBake/contact.html',{'msg': status_msg})

def product_details(request,id):
    status_msg = ''
    if request.method == 'POST':
       


        if 'customer' in request.session:
            price = request.POST['p_price']
            qty = request.POST['cart_qty']

            cart_exist = Cart.objects.filter(product = id, customer = request.session['customer'], status = 'pending').exists()
            if not cart_exist:
                cart = Cart(customer_id = request.session['customer'],
                            price = price, qty = qty, product_id = id)
                cart.save()
                return redirect('home_bake:cart')
            else:
                status_msg = 'Item Already in Cart'
        

        else:
            request.session['product_url'] = 'http://127.0.0.1:8000/product/'+str(id)
            # print(request.session['cart_item'])
            return redirect('home_bake:login','customer')

    product = Product.objects.get(id = id)
     
    return render(request,'HomeBake/product_details.html',{'product': product, 'msg': status_msg})

def my_cart(request):
    if 'customer' in request.session:
        cart_items = Cart.objects.filter(customer = request.session['customer'], status = 'pending')
        if cart_items:
            sum_total = Cart.objects.filter(customer = request.session['customer'], status = 'pending').aggregate(total =Sum(F('qty') * F('price')))
            customer = Customer.objects.get(id = request.session['customer'])
            print('summmm',sum_total)
            return render(request,'HomeBake/my_cart.html',{'cart_items': cart_items,'total': sum_total['total'], 'customer': customer})
    return render(request,'HomeBake/my_cart.html',)

def order_items(request):
    
    delivery_date = request.POST['delivery_date']
    shipping_address = request.POST['shipping_address']
    selected_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()
    current_date = date.today()
    status_code = 0
    
    min_expected= current_date + timedelta(days = 3)
    if  selected_date >= min_expected:
        if  selected_date >= min_expected:
            cart_items = Cart.objects.filter(customer = request.session['customer'], status = 'pending')
            for item in cart_items:
                item.delivery_date = delivery_date
                order_no = 'OD' + str(random.randint(1111111111,9999999999))

                item.order_no = order_no
                item.status = 'order placed'
                status_code = 201
                item.save()
                

            Cart.objects.filter(customer = request.session['customer']).update(delivery_date = delivery_date, 
                                                                                  status = 'order placed')
            Customer.objects.filter(id = request.session['customer']).update(address = shipping_address)
            
            
            return JsonResponse({'status': 'Order Placed', 'status_code': status_code})
        else:
            status_code = 403
            return JsonResponse({'status': 'Invalid Date Selection','status_code': status_code})

    else:
        status_code = 403
        return JsonResponse({'status': 'Invalid Date Selection', 'status_code': status_code})
        

     
    
def remove_cart(request,id):
    item = Cart.objects.get(id = id)
    item.delete()
    return redirect('home_bake:cart')
def my_account(request):
    return render(request,'HomeBake/account.html')

def my_orders(request):
    if 'customer' in request.session:
        order_list = Cart.objects.filter(customer = request.session['customer'])

        p = Paginator(order_list, 2) 
        page_number = request.GET.get('page')
        order_obj = p.get_page(page_number)
        return render(request,'HomeBake/my_orders.html',{'order_list': order_obj})
    return render(request,'HomeBake/my_orders.html')

@csrf_exempt
def create_checkout_session(request):
    data = json.loads(request.body)
    amount = data.get('amount', None)
    custom_amount = amount
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'inr',  # Replace with the currency code as needed (e.g., 'usd', 'eur', 'inr', etc.)
            'unit_amount': custom_amount,
            'product_data': {
                'name': '-',
                # You can add more product information if needed
            },
        },
        'quantity': 1,
    }],
    mode='payment',
    billing_address_collection='auto',
    success_url=YOUR_DOMAIN + '/',
    cancel_url=YOUR_DOMAIN + '/',

)   
    delivery_date = data.get('delivery_date', None)
    shipping_address = data.get('shipping_address', None)

    selected_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()
    current_date = date.today()
    
    
    min_expected= current_date + timedelta(days = 3)
    if  selected_date >= min_expected:
        if  selected_date >= min_expected:
            cart_items = Cart.objects.filter(customer = request.session['customer'], status = 'pending')
            for item in cart_items:
                item.delivery_date = delivery_date
                order_no = 'OD' + str(random.randint(1111111111,9999999999))

                item.order_no = order_no
                item.status = 'order placed'
                status_code = 201
                item.save()
                

            Cart.objects.filter(customer = request.session['customer']).update(delivery_date = delivery_date, 
                                                                                  status = 'order placed')
            Customer.objects.filter(id = request.session['customer']).update(address = shipping_address)
    

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
def stripe_webhook(request):

    print('WEBHOOK!')
    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = 'whsec_5895e8a8a572f0357da4049984a56ea7fdf32bc6d29ba99b8fb74c19eb81e557'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)

    return HttpResponse(status=200)



def logout(request):
    del request.session['customer']
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
                    customer = Customer.objects.get(id = request.session['customer'])
                    if customer.password == old_password:
                        customer.password = new_password
                        customer.save()
                        status_msg = 'Password Changed'

                    else:
                        status_msg = 'Password Incorrect'
                else:
                    status_msg = 'Password Does Not Match'
            else:
                status_msg = 'Password Should Be Minimum 8 Characters'


        except:
            status_msg = 'Incorrect Password'
    return render(request, 'HomeBake/change_password.html', {'msg': status_msg})