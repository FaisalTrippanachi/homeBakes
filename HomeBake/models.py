from django.db import models

# Create your models here.


class Seller(models.Model):
    seller_name = models.CharField(max_length = 30)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length = 100)
    gender = models.CharField(max_length = 15)
    address = models.CharField(max_length = 500)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 30)
    status = models.CharField(max_length = 20, default = 'pending')


    
    class Meta:
        db_table = 'seller_tb'

class Customer(models.Model):
    customer_name = models.CharField(max_length = 30)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length = 100)
    address = models.CharField(max_length = 500)
    password = models.CharField(max_length = 30)
   
    class Meta:
        db_table = 'customer_tb'