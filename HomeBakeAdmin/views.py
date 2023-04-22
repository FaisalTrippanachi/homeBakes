from django.shortcuts import redirect, render
from HomeBake.models import Seller,CustomerContact,Customer
import random
from django.core.paginator import Paginator
# Create your views here.


def dashboard(request):
    return render(request, 'HomeBakeAdmin/dashboard.html')


def sellers_list(request,status):
    sellers_list = Seller.objects.filter(status = status)
    return render(request, 'HomeBakeAdmin/sellers_list.html',{'sellers': sellers_list, 'status': status})

def users_msg(request):
    records = CustomerContact.objects.all()
    p = Paginator(records, 9)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    record_obj = p.get_page(page_number)
    
    return render(request, 'HomeBakeAdmin/users_msg.html',{'records': record_obj,})

def approve_Sellers(request, id):
    seller = Seller.objects.get(id = id)
    seller_id = random.randint(1111,9999)
    username = 'seller-' + str(seller.id) + str(seller_id)
    password = 'tmp-' + seller.seller_name.lower() + str(seller_id)
    seller.status = 'active'
    seller.username = username
    seller.password = password
    seller.save()
    return redirect('HomeBakeAdmin:sellers_list','pending')



