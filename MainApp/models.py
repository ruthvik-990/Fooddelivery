from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True)
    number=models.CharField(max_length=15,null=True,blank=True)
    
    class Meta:
        db_table="CustmerInfo"
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    def get_url(self):
        try:
            url=self.image.url
        except:
            url=""
        return url     
    class Meta:
        db_table="Restaurants_Info"    
class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
    transaction_id=models.CharField(max_length=100,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
    
    class Meta:
        db_table="OrderInfo"
    def __str__(self):
        return self.customer.name
    @property
    def get_cart_total(self):
        orderitems=self.orderitems_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitems_set.all()
        total=sum([item.quantity for item in orderitems])
        return total  
      


class Product(models.Model):
    name=models.TextField(max_length=50,null=True)
    price=models.DecimalField(max_digits=9,decimal_places=0)
    restaurant=models.ForeignKey(Restaurant,null=True,blank=True,on_delete=models.SET_NULL)
    image=models.ImageField(null=True,blank=True)

    def get_url(self):
        try:
            url=self.image.url
        except:
            url=""
        return url        
    
    class Meta:
        db_table="ProductInfo"
    def __str__(self):
        return self.name

class OrderItems(models.Model):
    order=models.ForeignKey(Order,null=True,blank=True,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
    
    quantity=models.IntegerField(default=0)
    date_item_added=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="OrderItemInfo"

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total    
    @property
    def get_count(self):
        return self.quantity    


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address        
