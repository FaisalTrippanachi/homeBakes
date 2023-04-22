from django.db import models
from datetime import date
 
# Create your models here.


class Seller(models.Model):
    seller_name = models.CharField(max_length = 30)
    zipcode = models.CharField(max_length = 30)
    location = models.CharField(max_length = 30, default = '')
    phone = models.BigIntegerField()
    email = models.EmailField(max_length = 100)
    address = models.CharField(max_length = 500)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 30)
    status = models.CharField(max_length = 20, default = 'pending')


    
    class Meta:
        db_table = 'seller_tb'

class Product(models.Model):
    product_name = models.CharField(max_length = 50)
    category = models.CharField(max_length = 30, default = '')
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    ingredients_used = models.CharField(max_length = 200)
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'product/')
    status = models.CharField(max_length = 30, default = 'available')
    

    class Meta:
        db_table = 'product'

class Customer(models.Model):
    customer_name = models.CharField(max_length = 30)
    phone = models.BigIntegerField()
    zipcode = models.CharField(max_length = 30)
    location = models.CharField(max_length = 30, default = '')

    email = models.EmailField(max_length = 100)
    address = models.CharField(max_length = 500)
    password = models.CharField(max_length = 30)
   
    class Meta:
        db_table = 'customer_tb'

class CustomerContact(models.Model):
    customer_name = models.CharField(max_length = 30)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length = 100)
    message = models.CharField(max_length = 500)
    date = models.CharField(max_length = 30)
    
   
    class Meta:
        db_table = 'contact_tb'


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    order_date = models.CharField(max_length = 30, default = date.today)
    order_no = models.CharField(max_length = 50, default = '')
    order_id = models.IntegerField(default = 0)
    qty = models.FloatField()
    price = models.FloatField()
    delivery_date = models.CharField(max_length = 30, default = '')
    status = models.CharField(max_length = 20, default = 'pending')

    def product_total(self):
        return self.qty * self.price

    class Meta:
        db_table = 'cart_tb' 