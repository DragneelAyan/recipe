from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def recipeview(request):  
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )       
        return redirect('recipes')
    
    queryset = Recipe.objects.all()
    context = {'recipes': queryset}
    
    return render(request, 'recipes.html', context)


@login_required(login_url='login')
def deleterecipe(request, id):
    Recipe.objects.filter(id=id).delete()
    return redirect('recipes')


@login_required(login_url='login')
def updaterecipe(request, id):
    queryset = Recipe.objects.get(id=id)
    
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        
        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image
            
        queryset.save()
        return redirect('recipes')
    
    context = {'recipe': queryset}
    return render(request, 'updaterecipes.html', context)


def registerpage(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'Username is already taken')
            return redirect('register')
        
        user = User.objects.create(
            first_name = firstname,
            last_name = lastname,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('recipes')
    
    return render(request, 'register.html')


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, 'Invalid Username')
            return redirect('login')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        else:
            login(request, user)
            return redirect('recipes')
        
    return render(request, 'login.html') 


def logoutpage(request):
    logout(request)
    return redirect('login')