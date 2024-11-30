from django.db import models
from django.contrib.auth.models import User

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


