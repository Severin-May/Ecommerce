from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Product, Order, Client, Profile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Profile)
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)