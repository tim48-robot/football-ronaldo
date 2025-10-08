import datetime
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Product
from django.core import serializers
from main.forms import ProductForm


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})
    
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "message": "Registration successful!"})
    
    # Format errors for better display
    errors = {}
    for field, error_list in form.errors.items():
        errors[field] = [str(error) for error in error_list]
    
    return JsonResponse({"success": False, "errors": errors}, status=400)


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == "GET":
        form = AuthenticationForm(request)
        return render(request, "login.html", {"form": form})
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        auth_login(request, user)
        response = JsonResponse({"success": True, "message": "Login successful!"})
        response.set_cookie("last_login", str(datetime.datetime.now()))
        return response
    
    return JsonResponse({
        "success": False, 
        "message": "Invalid username or password."
    }, status=400)


@login_required(login_url='/login')
def logout_user(request):
    if request.method == "POST":
        auth_logout(request)
        response = JsonResponse({"success": True, "message": "Logout successful!"})
        response.delete_cookie('last_login')
        return response
    
    # Fallback for GET request
    auth_logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)
    
    context = {
        'nama_aplikasi': 'Football Product',
        'name': request.user.username,
        'class': 'PBP D',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)


@login_required(login_url='/login')
@require_http_methods(["POST"])
def create_product(request):
    form = ProductForm(request.POST or None)
    
    if form.is_valid():
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        
        return JsonResponse({
            "success": True,
            "message": "Product created successfully!",
            "product": {
                "id": str(product_entry.id),
                "name": product_entry.name,
                "price": product_entry.price,
                "description": product_entry.description,
                "views": getattr(product_entry, "views", 0),
                "category": product_entry.get_category_display(),
                "is_featured": product_entry.is_featured,
            }
        })
    
    # Format errors for better display
    errors = {}
    for field, error_list in form.errors.items():
        errors[field] = [str(error) for error in error_list]
    
    return JsonResponse({"success": False, "errors": errors}, status=400)


@login_required(login_url='/login')
@require_http_methods(["POST"])
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    form = ProductForm(request.POST or None, instance=product)
    
    if form.is_valid():
        form.save()
        return JsonResponse({
            "success": True,
            "message": "Product updated successfully!",
            "product": {
                "id": str(product.id),
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "views": getattr(product, "views", 0),
                "category": product.get_category_display(),
                "is_featured": product.is_featured,
            }
        })
    
    # Format errors for better display
    errors = {}
    for field, error_list in form.errors.items():
        errors[field] = [str(error) for error in error_list]
    
    return JsonResponse({"success": False, "errors": errors}, status=400)


@login_required(login_url='/login')
@require_http_methods(["POST", "DELETE"])
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product_name = product.name
    product.delete()
    
    return JsonResponse({
        "success": True, 
        "message": f"Product '{product_name}' deleted successfully!"
    })


@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    # Increment views
    if hasattr(product, "increment_views"):
        try:
            product.increment_views()
        except Exception:
            pass
    
    return JsonResponse({
        "success": True,
        "product": {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "views": getattr(product, "views", 0),
            "category": product.get_category_display(),
            "is_featured": product.is_featured,
            "thumbnail": product.thumbnail or "",
        }
    })


def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, product_id):
    product_item = Product.objects.filter(pk=product_id)
    xml_data = serializers.serialize("xml", product_item)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json_by_id(request, product_id):
    product_item = Product.objects.filter(pk=product_id)
    json_data = serializers.serialize("json", product_item)
    return HttpResponse(json_data, content_type="application/json")