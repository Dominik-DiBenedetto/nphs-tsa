from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import Member

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not Member.objects.filter(username=username).exists() and not Member.objects.filter(email=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username or Email')
            return redirect('/auth/login/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/auth/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/home/')

    # Render the login page template (GET request)
    return render(request, 'auth/login.html')

# Define a view function for the registration page
def register_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        name = request.POST.get('name')
        n_num = request.POST.get('nnumber')
        email = request.POST.get('email')

        password = request.POST.get('password')
        conf_password = request.POST.get('confirm-password')

        
        # Check if a user with the provided username already exists
        user = Member.objects.filter(username=n_num)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "nNumber already in use!")
            return redirect('/auth/register/')

        if password != conf_password:
            # Display an information message if the password doesnt match the confirmation passcode is taken
            messages.info(request, "Passwords don't match!")
            return redirect('/auth/register/')
        
        # Create a new User object with the provided information
        user = Member.objects.create_user(
            name=name,
            username=n_num,
            email=email,
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")

        login(request, user)

        return redirect('/home/')
    
    # Render the registration page template (GET request)
    return render(request, 'auth/register.html')