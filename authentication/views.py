from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import Member, CustomUserUpdateForm
from django.contrib.auth.models import Group, Permission
from django.core.serializers import serialize
from django.contrib.auth.decorators import user_passes_test
import json
from django.views.decorators.csrf import csrf_protect

officer_nnumbers = {
    "N463506": "President",
    "N501029": "Vice President",
    "N432119": "Secretary",
    "N443333": "Treasurer",
    "N431784": "Reporter",
    "N434205": "Sergeant At Arms",
}

officer_names = {
    "N463506": "Bella Ramsey",
    "N501029": "Dominik DiBenedetto",
    "N432119": "Megan Taylor",
    "N443333": "Alexander Avin",
    "N431784": "Elizabeth Carpenter",
    "N434205": "Michael Dankanich",
}

def update_roles(user):
    officer_permissions_group, created = Group.objects.get_or_create(name='Officer')
    for n_num, role in officer_nnumbers.items():
        if user.username != n_num: continue
        user.role = role
        user.groups.add(officer_permissions_group)
        user.name = officer_names[n_num]
        user.is_active = True
        
        user.save()

def is_officer(user):
    return user.is_superuser or user.groups.filter(name="Officer").exists()

# Create your views here.
@csrf_protect
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username').upper() #nnumber or email
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
            update_roles(user)
            return redirect('/home/')

    # Render the login page template (GET request)
    return render(request, 'auth/login.html')

# Define a view function for the registration page
@csrf_protect
def register_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        name = request.POST.get('name').title()
        n_num = request.POST.get('nnumber').upper()
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
        user.is_active = False
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully, once your dues are paid you will be approved and able to login!")

        login(request, user)
        update_roles(user)

        return redirect('/home/')
    
    # Render the registration page template (GET request)
    return render(request, 'auth/register.html')

@user_passes_test(is_officer)
def approve_users(request):
    users = Member.objects.all()
    data = list(users.values()) 
    if request.method == "POST":
        body_data = json.loads(request.body)
        if body_data:
            n_num = body_data["n_num"]

            user = get_object_or_404(Member, username=n_num)
            if user:
                user.is_active = True
                user.save()

    return render(request, "auth/approve.html", {"users_list": data})

@user_passes_test(is_officer)
def deny_user(request):
    if request.method == "POST":
        n_num = json.loads(request.body)["n_num"]

        user = get_object_or_404(Member, username=n_num)
        if user:
            user.delete()
        return redirect("/auth/approve/")
        
    return redirect("/auth/approve/")

def logout_view(request):
    logout(request)
    return redirect("/home/")