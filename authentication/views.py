from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def login(request):
    print("\n" + "="*50)
    print("LOGIN REQUEST RECEIVED")
    print("="*50)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f"✅ JSON Parsed - Username: '{username}'")
        except json.JSONDecodeError:
            # Handle form data properly
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(f"Using POST data - Username: '{username}', Password: {'*' * len(password) if password else 'None'}")
        
        print(f"Attempting to authenticate user: '{username}'")
        print(f"Password received: {'Yes' if password else 'No'}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"✅ User authenticated: {user.username}")
            if user.is_active:
                auth_login(request, user)
                print(f"✅ User logged in successfully")
                return JsonResponse({
                    "username": user.username,
                    "status": "success",
                    "message": "Login successful!"
                }, status=200)
            else:
                print(f"❌ User is not active")
                return JsonResponse({
                    "status": "failed",
                    "message": "Login failed, account is disabled."
                }, status=401)
        else:
            print(f"❌ Authentication failed for username: '{username}'")
            return JsonResponse({
                "status": "failed",
                "message": "Login failed, please check your username or password."
            }, status=401)
    
    return JsonResponse({
        "status": "failed",
        "message": "Invalid request method."
    }, status=400)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)


@csrf_exempt
def logout(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)