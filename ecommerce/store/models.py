from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=3, max_digits=7)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=3, max_digits=7)
    description = models.CharField(max_length=300, default='Product has no description', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.name

class Client(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=70)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length= 150, default='Mountain View', blank=True)
    quantity = models.IntegerField(default=1)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} {self.quantity}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    modification_date = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=150, blank=True)
    address2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(max_length=150, blank=True)
    old_cart = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):

    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

