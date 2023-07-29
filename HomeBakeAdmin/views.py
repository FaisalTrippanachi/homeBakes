from django.shortcuts import redirect, render
from HomeBake.models import Seller,CustomerContact,Customer,Admin
import random
from django.core.paginator import Paginator
from datetime import date
from .decorator import auth_admin
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

@auth_admin
def dashboard(request):
    customer_count = Customer.objects.all().count()
    pending_seller_count = Seller.objects.filter(status = 'pending').count()
    active_seller_count = Seller.objects.filter(status = 'active').count()

    current_date = date.today()
    print(current_date)
    enquiry_today = CustomerContact.objects.filter(date = current_date).count()
    context = {
        'customer_count': customer_count,
        'pending_seller_count': pending_seller_count,
        'active_seller_count': active_seller_count,
        'enquiry_today': enquiry_today
    }
    return render(request, 'HomeBakeAdmin/dashboard.html', context)

@auth_admin
def sellers_list(request,status):
    sellers_list = Seller.objects.filter(status = status)
    p = Paginator(sellers_list, 2) 
    page_number = request.GET.get('page')
    seller_obj = p.get_page(page_number)
    return render(request, 'HomeBakeAdmin/sellers_list.html',{'sellers': seller_obj, 'status': status})

@auth_admin
def customers_list(request):
    customers_list = Customer.objects.all()
    p = Paginator(customers_list, 2) 
    page_number = request.GET.get('page')
    customer_obj = p.get_page(page_number)
    return render(request, 'HomeBakeAdmin/customers_list.html',{'customers': customer_obj,})

@auth_admin
def enquiry(request):
    records = CustomerContact.objects.all().order_by('-id')
    p = Paginator(records, 9)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    record_obj = p.get_page(page_number)
    
    return render(request, 'HomeBakeAdmin/enquiry.html',{'records': record_obj,})

@auth_admin
def approve_Sellers(request, id):
    seller = Seller.objects.get(id = id)
    seller_id = random.randint(1111,9999)
    username = 'seller-' + str(seller.id) + str(seller_id)
    password = 'tmp-' + seller.seller_name.lower() + str(seller_id)
    hashed_password = make_password(password)
    seller.status = 'active'
    seller.username = username
    seller.password = hashed_password
    seller.save()

    message = 'Thank you for registering, your account username is '+ username + 'and password is ' +password

    send_mail(
        subject = 'Your account was Approved',
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [seller.email]
    ) 
    return redirect('HomeBakeAdmin:sellers_list','pending')

@auth_admin
def change_password(request):
    status_msg = ''
    if request.method  == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        try:
            if len(new_password) > 8:
                if new_password == confirm_password:
                    admin = Admin.objects.get(id = request.session['admin'])
                    if admin.password == old_password:
                        admin.password = new_password
                        admin.save()
                        status_msg = 'Password Changed'

                    else:
                        status_msg = 'Password Incorrect'
                else:
                    status_msg = 'Password Does Not Match'
            else:
                status_msg = 'Password Should Be Minimum 8 Characters'


        except:
            status_msg = 'Incorrect Password'
    return render(request, 'HomeBakeAdmin/change_password.html', {'msg': status_msg})
def logout(request):
    del request.session['admin']
    request.session.flush()
    return redirect('home_bake:customer_home')



