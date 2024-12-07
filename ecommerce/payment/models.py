from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.dispatch import receiver
import datetime
from django.db.models.signals import post_save, pre_save

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ship_full_name = models.CharField(max_length=200)
    ship_email = models.CharField(max_length=200)
    ship_address1 = models.CharField(max_length=200)
    ship_address2 = models.CharField(max_length=200, null=True, blank=True)
    ship_city = models.CharField(max_length=200)
    ship_state = models.CharField(max_length=200, null=True, blank=True)
    ship_zipcode = models.CharField(max_length=200, null=True, blank=True)
    ship_country = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_shipped = models.DateTimeField(null=True, blank=True)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order - {str(self.id)}'

@receiver(pre_save,sender=Order)
def ship_date_update(sender, instance, **kwargs):
    if instance.pk:
        curr_time = datetime.datetime.now()
        send = sender._default_manager.get(pk=instance.pk)
        if instance.is_shipped and not send.is_shipped:
            instance.date_shipped = curr_time


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'

def create_shipping(sender, instance, created, **kwargs):

    if created:
        user_ship = ShippingAddress(user=instance)
        user_ship.save()

post_save.connect(create_shipping, sender=User)




