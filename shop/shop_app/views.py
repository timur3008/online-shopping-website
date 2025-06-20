from . import models
from .forms import AuthorizationForm, RegistrationForm, CommentForm
from .utils import get_cart_data, CartForUser

from django.http import HttpRequest
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def render_home_page(request: HttpRequest):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    slides = models.Slider.objects.all()
    page = request.GET.get('page')

    paginator = Paginator(products, 4)
    products = paginator.get_page(page)

    if request.user.is_authenticated:
        favorite_products = models.ProductFavorite.objects.filter(user=request.user)
        favorite_products = [item.product.pk for item in favorite_products]
    else:
        favorite_products = []

    context = {
        'categories': categories,
        'products': products,
        'slides': slides,
        'favorite_products': favorite_products
    }

    return render(request, 'index.html', context)

def search_products(request: HttpRequest):
    search_data = request.GET.get('query')
    categories = models.Category.objects.all()

    if search_data:
        products = models.Product.objects.filter(name__iregex=search_data)
    else:
        products = models.Product.objects.all()

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'products_list.html', context)

def render_products_list_page(request: HttpRequest):
    category_query = request.GET.get('category')
    categories = models.Category.objects.all()
    products = models.Product.objects.all()

    if category_query:
        products = products.filter(category__slug=category_query)

    page = request.GET.get('page')
    paginator = Paginator(products, 3)
    products = paginator.get_page(page)

    if request.user.is_authenticated:
        favorite_products = models.ProductFavorite.objects.filter(user=request.user)
        favorite_products = [item.product.pk for item in favorite_products]
    else:
        favorite_products = []

    context = {
        'categories': categories,
        'products': products,
        'category_query': category_query,
        'favorite_products': favorite_products
    }

    return render(request, 'products_list.html', context)

def render_product_detail_page(request: HttpRequest, product_id: int):
    product = models.Product.objects.get(pk=product_id)

    if request.user.is_authenticated:
        favorite_products = models.ProductFavorite.objects.filter(user=request.user)
        favorite_products = [item.product.pk for item in favorite_products]
    else:
        favorite_products = []

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.product = product
            comment_form.author = request.user
            comment_form.save()
            messages.success(request, 'Спасибо за ваш отзыв!!!')
            return redirect(request.META.get('HTTP_REFERER', 'home_path'))
    else:
        comment_form = CommentForm()

    context = {
        'product': product,
        'comment_form': comment_form,
        'favorite_products': favorite_products
    }

    return render(request, 'product_detail.html', context)

def render_authorization_page(request: HttpRequest):
    if request.method == 'POST':
        form = AuthorizationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно зашли в аккаунт!!!')
                return redirect('home_path')
            else:
                messages.warning(request, 'Пользователь с такими данными не найден!!!')
        else:
            messages.warning(request, 'Вы указали неправильные данные!!!')
    else:
        form = AuthorizationForm()

    context = {
        'form': form
    }

    return render(request, 'authorization.html', context)

def render_registration_page(request: HttpRequest):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!!!')
            return redirect('authorization_path')
        else:
            messages.warning(request, 'Введение неправильные данные!!!')
    else: 
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'registration.html', context)

def render_logout_page(request: HttpRequest):
    logout(request)
    messages.warning(request, 'Вы вышли со своего аккаунта!!!')
    return redirect('home_path')

def render_wishlist_page(request: HttpRequest):
    products = request.user.favorite_products.all()
    categories = models.Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'wishlist.html', context)

@login_required(login_url='/authorization/')
def activate_favourite(request: HttpRequest, product_id: int):
    product = models.Product.objects.get(pk=product_id)
    user = request.user

    is_liked = models.ProductFavorite.objects.filter(user=user, product=product).exists()

    if is_liked:
        favorite_product = models.ProductFavorite.objects.get(user=user, product=product)
        favorite_product.delete()
        messages.warning(request, f'Вы убрали {product.name} со списка желаний!!!')
    else:
        favorite_product = models.ProductFavorite.objects.create(user=user, product=product)
        favorite_product.save()
        messages.success(request, f'Вы добавили {product.name} в список желаний!!!')

    return redirect(request.META.get('HTTP_REFERER', 'products_list_path'))

def render_cart_page(request: HttpRequest):
    cart_info = get_cart_data(request)

    context = {
        'title': 'Моя корзина',
        'cart': cart_info['cart'],
        'cart_products': cart_info['cart_products']
    }

    return render(request, 'cart.html', context)

@login_required(login_url='/authorization/')
def update_cart(request: HttpRequest, product_id: int, action: str, quantity: int = 1):
    cart = CartForUser(request)
    cart.add_or_delete(product_id=product_id, quantity=quantity, action=action)
    if action == 'add':
        messages.success(request, 'Продукт успешно добавлен в корзину!!!')
    else:
        messages.warning(request, 'Продукт удален с корзины!!!')

    return redirect(request.META.get('HTTP_REFERER', 'home_path'))