from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


def home(request):
    
    return render(request, 'account/index.html')

def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('my_login')

    context = {'RegisterForm': form}

    return render(request, 'account/register.html', context)


def my_login(request):

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')  # username is the email
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_software_engineer == True:

                login(request, user)
                return redirect('software_engineer-dashboard')
            
            if user is not None and user.is_software_engineer == False:

                login(request, user)
                return redirect('client-dashboard')
            
    context = {'LoginForm': form}
    return render(request, 'account/my_login.html', context)

def user_logout(request):
    logout(request)
    return redirect('my_login')






