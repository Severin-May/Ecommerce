from distutils.command.install import install
from itertools import product

from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateProfileForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error, please, try again!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out, bro!")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registered, bro! Now fill out the personal info!")
            return redirect('update_profile_info')
        else:
            messages.success(request, "Oooppsi, there is a problem with registration, bro!")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category' : category})
    except:
        messages.success(request, "This category does not exist, bro!")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})

def update_profile(request):
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

def update_password(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            update_password_form = ChangePasswordForm(user, request.POST)

            if update_password_form.is_valid():
                update_password_form.save()
                messages.success(request, "You have changed your password!!!")

                login(request, user)
                return redirect('update_profile')
            else:
                for error in list(update_password_form.errors.values()):
                    messages.error(request, error)
        else:
            update_password_form = ChangePasswordForm(user)

        return render(request, 'update_password.html', {'update_password_form': update_password_form})
    else:
        messages.success(request, "You should be logged in to edit the password!!!")
        return redirect('home')


def update_profile_info(request):
    if request.user.is_authenticated:
        user = Profile.objects.get(user__id=request.user.id)
        update_profile_info_form = UserInfoForm(request.POST or None, instance=user)

        if update_profile_info_form.is_valid():
            update_profile_info_form.save()

            messages.success(request, "User info has been updated")
            return render(request, 'home.html', {})
        return render(request, 'update_profile_info.html', {'update_profile_info_form': update_profile_info_form})
    else:
        messages.success(request, "You should be logged in to edit the user info!!!")
        return render(request, 'home.html', {})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.error(request, "The searched product does not exist!")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        pass

    return render(request, 'search.html', {})