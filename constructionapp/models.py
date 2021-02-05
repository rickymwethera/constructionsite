from django.db import models
from django.utils import timezone
from phone_field import PhoneField
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    my_location  = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile/', default='a.png')
    
    
    def __str__(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length =30)

    def __str__(self):
        return self.name 

    @classmethod
    def get_category(cls):
        categorys = Category.objects.all()
        return categorys       

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete() 

class Product(models.Model):
    name = models.CharField(max_length=250, blank=True)
    product_pic = models.ImageField(upload_to='products/')
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)

    # def get_cart_items(self):
    #     orderItem = self.orderItem_set.all()
    #     return self.orderItem.all()

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    # def __str__(self):
    #     return self.product.name
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=500, blank=True, default='Worth the Price')
    date = models.DateTimeField(auto_now_add=True, blank=True) 

    def __str__(self):
        return f'{self.image.name} comment'

    class Meta:
        ordering = ["-pk"]


    @classmethod
    def update_comment(cls,id,new_comment):
        cls.objects.filter(id=id).update(comment = new_comment)
        
    @classmethod
    def get_comments(cls,id):
        comments = cls.objects.filter(image__id=id)
        return comments
    

    @classmethod
    def delete_comment(cls,id):
        cls.objects.filter(id).delete()

class ShippingAddress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    estate = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address