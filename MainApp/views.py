from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
###
from django.contrib.auth.decorators import login_required
###
from django.contrib.auth.hashers import check_password

# Create your views here.

def landing(request):
    return render(request, 'MainApp/landing.html')

# def login_user(request):
#     return render(request, 'MainApp/login.html')

# def register_user(request):
#     return render(request, 'MainApp/register.html')

@login_required(login_url='login')
def Home(request):
    return render(request, 'MainApp/Home.html')

@login_required(login_url='login')
def Bookmarks(request):
    return render(request, 'MainApp/Bookmarks.html')

@login_required(login_url='login')
def Profile(request):
    return render(request, 'MainApp/Profile.html')

@login_required(login_url='login')
def MyExperiences(request):
    return render(request, 'MainApp/MyExperiences.html')

def register_user(request):
    if request.method == 'POST':
        # Get Post Parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        # Checking if username already exists
        userex = User.objects.filter(username=username)
        if userex.exists():
            messages.error(request,'Username already exists!! Enter a unique username.')
            return redirect('register')

        emailex = User.objects.filter(email=email)
        if emailex.exists():
            messages.error(request,'This email address is already registered!! Please Login.')
            return redirect('login')

        # Checks
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters !!")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must only contain letters and numbers !!")
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Confirm password do not match with password !!")
            return redirect('register')

        
        # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        user = authenticate(username=username, password=pass1)
        login(request,user)
        messages.success(request,'Your account has been successfully created !!')
        return redirect('Home')

    else:
        return render(request, 'MainApp/register.html')


def login_user(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfully logged in !!")
            return redirect('Home')
        else:
            messages.error(request,("Invalid Credentials!! Please try again or register."))
            return redirect('login')
    else:
        return render(request, 'MainApp/login.html')

def logout_user(request):
    logout(request)
    return redirect('landing')

###
def password_reset(request):
    if request.method == 'POST':
        pass3 = request.POST['pass3']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        userpassword = request.user.password
        current_user = request.user.id
        userobj = User.objects.get(id=current_user)
        matchcheck = check_password(pass3,userpassword)

        # Checks
        if pass1 != pass2:
            messages.error(request, "Confirm new password do not match with new password !!")
            return redirect('password_reset')
        ##

        if matchcheck:
            userobj.set_password(pass1)
            userobj.save()
            messages.success(request, "Password changed successfully !!")
            user = authenticate(username=userobj.username, password=pass1)
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request, "Existing current password do not match with entered current password !!")
            return redirect('password_reset')

    else:
        return render(request, 'MainApp/Password_reset.html')
        

