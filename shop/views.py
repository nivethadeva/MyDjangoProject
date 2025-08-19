from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib import messages
from .models import Product
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def home(request):
    products = Product.objects.all()
    return render(request, "shop/home.html", {
        "products": products})

def category_products(request, category_name):
    products = Product.objects.filter(category__iexact=category_name)
    return render(request, 'shop/category_products.html', {
        'category_name': category_name,
        'products': products
    })

def buy_now(request, id):
    product = Product.objects.get(id=id)
    # handle buy now logic here
    return redirect('shop:checkout')  # or your checkout page

def product_search(request):
    query = request.GET.get('q', '')
    # Search in name and category
    results = Product.objects.filter(name__icontains=query) | Product.objects.filter(category__icontains=query)
    return render(request, 'shop/search_results.html', {'products': results, 'query': query})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('shop:login')

    return render(request, 'shop/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')   # ✅ corrected
        password2 = request.POST.get('password2')   # ✅ corrected
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        # create user with hashed password
        user = User.objects.create_user(username=username, password=password1, email=email)
        user.save()
        messages.success(request, "Successfully Registered!")
        return redirect('shop:login')

    return render(request, 'shop/register.html')


    
def logout_view(request):
    logout(request)
    return redirect('shop:home')

def cart_view(request):
    return render(request, 'shop/cart.html')


def category_view(request, category_name):
    products = Product.objects.filter(category__iexact=category_name)
    return render(request, 'shop/category.html', {
        'category': category_name,
        'products': products
    })

def product_list(request):
    # Example product data
    products = {
        1: {'name': 'Red Dress', 'price': 500, 'image': '/media/red_dress.jpg'},
        2: {'name': 'Blue Saree', 'price': 700, 'image': '/media/blue_saree.jpg'},
        3: {'name': 'Yellow Top', 'price': 300, 'image': '/media/yellow_top.jpg'},
    }
    context = {'products': products}
    return render(request, 'shop/add_to_cart.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# Product list page
def product_list(request):
    return render(request, 'shop/product_list.html', {'products': products})


def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'shop/cart.html', {'cart_items': cart, 'total_price': total_price})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart!")
    return redirect('shop:cart')  # <-- This name must match urls.py

def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found!")
        return redirect('shop:product_list')

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url,
            'quantity': 1,
        }

    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to cart!")

    # ✅ Redirect back to same page
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("shop:product_list")