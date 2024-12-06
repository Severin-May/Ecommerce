from distutils.command.install import install
from itertools import product
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateProfileForm, UpdatePasswordForm, UserInfoForm
from .models import Product, Category, Profile
from django.db.models import Q
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            curr_user = Profile.objects.get(user__id=request.user.id)
            old_cart = curr_user.old_cart
            if old_cart:
                json_cart = json.loads(old_cart)
                cart = Cart(request)

                for key, value in json_cart.items():
                    cart.db_add(product=key,quantity=value)
            messages.success(request, "You successfully logged in!")
            return redirect('home')
        else:
            messages.success(request, "Login was unsuccessful, please, try again!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out, bro!")
    return redirect('home')

def user_register(request):
    register_form = SignUpForm()
    if request.method == "POST":
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registered, bro! Now fill out the personal info!")
            return redirect('update_profile_info')
        else:
            messages.success(request, "Oooppsi, there is a problem with registration!")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': register_form})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        cat = Category.objects.get(name=foo)
        prods = Product.objects.filter(category=cat)
        return render(request, 'category.html', {'products': prods, 'category' : cat})
    except Category.DoesNotExist:
        messages.success(request, "This category does not exist!")
        return redirect('home')
    except Exception as e:
        # Catch other unexpected exceptions, log and show a general error
        messages.error(request, "An unexpected error occurred.")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def profile_update(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        update_profile_form = UpdateProfileForm(request.POST or None, instance=user)

        if update_profile_form.is_valid():
            update_profile_form.save()

            login(request, user)
            messages.success(request, "User profile has been updated")
            return render(request, 'home.html', {})
        return render(request, 'update_profile.html', {'update_profile_form': update_profile_form})
    else:
        messages.success(request, "You should be logged in to edit the profile!!!")
        return render(request, 'home.html', {})

def password_update(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            update_password_form = UpdatePasswordForm(user, request.POST)

            if update_password_form.is_valid():
                update_password_form.save()
                messages.success(request, "You have changed your password!!!")

                login(request, user)
                return redirect('update_profile')
            else:
                for error in list(update_password_form.errors.values()):
                    messages.error(request, error)
        else:
            update_password_form = UpdatePasswordForm(user)
            return render(request, 'update_password.html', {'update_password_form': update_password_form})
    else:
        messages.success(request, "You should be logged in to edit the password!!!")
        return redirect('home')


def profile_info_update(request):
    if request.user.is_authenticated:
        user = Profile.objects.get(user__id=request.user.id)
        update_profile_info_form = UserInfoForm(request.POST or None, instance=user)

        shipping_user = ShippingAddress.objects.get(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if update_profile_info_form.is_valid() or shipping_form.is_valid():
            update_profile_info_form.save()
            shipping_form.save()

            messages.success(request, "User Profile Info has been updated")
            return render(request, 'home.html', {})
        return render(request, 'update_profile_info.html', {'update_profile_info_form': update_profile_info_form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You should be logged in to edit the user profile info!!!")
        return render(request, 'home.html', {})

def search(request):
    if request.method == "POST":
        search_key = request.POST['searched']
        search_key = Product.objects.filter(Q(name__icontains=search_key) | Q(description__icontains=search_key))

        if not search_key:
            messages.error(request, "The searched item does not exist!")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': search_key})
    else:
        pass

    return render(request, 'search.html', {})