from django.db import models
from django.db.models.base import Model
# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    pub_date = models.DateField()
    subcategory = models.CharField(max_length=30)
    image = models.ImageField(upload_to='shop/images' , default ='')

    def __str__(self):
        return self.product_name
        
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50 , default='')
    email = models.CharField(max_length=50 , default='')
    number = models.CharField(max_length=10 , default='')
    desc = models.CharField(max_length=550,default='')

    def __str__(self) :
        return self.name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000,default='')
    name = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=50,default='')
    number = models.CharField(max_length=10,default='')
    address = models.CharField(max_length=200,default='')
    city = models.CharField(max_length=50,default='')
    state = models.CharField(max_length=50,default='')
    zip_code = models.CharField(max_length=7,default='')
   
    def __str__(self):
        return self.name

class order_update(models.Model):
    update_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    order_id = models.IntegerField( default='')
    update_desc = models.CharField(max_length=1000,default='')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        orders_id = str(self.order_id)
        return orders_id

        