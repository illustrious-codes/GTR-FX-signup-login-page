
from email import message
from os import name
from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Room, Message, UserStatus
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth import logout as logouts

# Create your views here.
def home(request):
    return render(request, 'home.html')


def checkview(request):
    if request.method == 'POST':
        # room = request.POST.get('room_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if not Room.objects.filter(name=room).exists():
        #     messages.error(request, "User ID does not exist.")
        #     return redirect('checkview') 
            # new_room = Room.objects.create(name=room)
            # new_room.save()
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist.")
            return redirect('home') 
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid user ID or password.")
            return redirect('home')
        login(request, user)
        # return redirect(f'/{room}/?username={username}')
        return render(request, 'room.html')
    return render(request, 'home.html')






def create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not password2:
            messages.error(request, "All fields are required.")
            return redirect('create')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('create')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists.")
            return redirect('create')

        try:
            validate_slug(username)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "User created successfully.")
            return redirect('home')
        except ValidationError:
            messages.error(request, "Invalid username format.")
            return redirect('create')
    else:
        return render(request, 'create.html')
    
def logout(request):
    logouts(request)
    return redirect('/')

