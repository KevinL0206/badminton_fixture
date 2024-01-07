from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, loginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def startPageRedirect(request):
    return redirect('register')

def register(request):
    form = CreateUserForm()
    context = {'form':form}

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Successful')
            return redirect('login')
        

    return render(request,'register.html',context)

def loginUser(request):
    form = loginForm()
    context = {'form':form}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
            ...
        else:
            messages.success(request, 'Login Failed')
            return redirect('login')
            # Return an 'invalid login' error message.
    else:
        return render(request,'login.html',context)
    
def logoutUser(request):
    logout(request)
    messages.success(request, 'You Were Logged Out')
    return redirect('login')
    
def home(request):

    user = request.user
    context = {'user':user}

    return render(request,'home.html',context)