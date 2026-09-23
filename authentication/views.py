import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

from django.views.decorators.csrf import csrf_protect

from .models import Member

# Helper functions
def is_officer(user):
    return user.is_superuser or user.groups.filter(name="Officer").exists()

# Views
@csrf_protect
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method != "POST": return render(request, 'auth/login.html')

    username = request.POST.get('username').upper().strip() #nnumber
    password = request.POST.get('password').strip()

    if not Member.objects.filter(username=username).exists() and not Member.objects.filter(username=username.lower()).exists():
        messages.error(request, 'Invalid N-Number')
        return redirect('/auth/login/')
    
    user = authenticate(username=username, password=password) or authenticate(username=username.lower(), password=password)
    
    if user is None:
        messages.error(request, "Invalid Password")
        return redirect('/auth/login/')
    
    login(request, user)
    return redirect('/home/')

@csrf_protect
def register_page(request):
    if request.user.is_authenticated: return redirect('/home/')
    if request.method != "POST":  return render(request, 'auth/register.html')

    n_num = request.POST.get('nnumber').upper().strip()
    if not "N" in n_num:  n_num = "N" + n_num

    password = request.POST.get('password').strip()
    conf_password = request.POST.get('confirm-password').strip()
    if password != conf_password:
        messages.info(request, "Passwords don't match!")
        return redirect('/auth/register/')

    user = Member.objects.filter(username=n_num)
    if user.exists():
        messages.info(request, "nNumber already in use!")
        return redirect('/auth/register/')

    name = request.POST.get('name').title().strip()
    email = request.POST.get('email').strip()
    user = Member.objects.create_user(
        name=name,
        username=n_num,
        email=email,
    )
    
    user.set_password(password)
    user.is_active = False
    user.save()
    
    messages.info(request, "Account created Successfully, once your dues are paid you will be approved and able to login!")

    login(request, user)

    return redirect('/home/')

def logout_view(request):
    logout(request)
    return redirect("/home/")

# Officer only views
@user_passes_test(is_officer)
def approve_users(request):
    users = Member.objects.all()
    data = list(users.values()) 
    if request.method == "POST":
        body_data = json.loads(request.body)
        if not body_data: 
            messages.info(request, "Bad request!")
            return render(request, "auth/approve.html", {"users_list": data})
        
        n_num = body_data["n_num"]
        user = get_object_or_404(Member, username=n_num)
        if not user:
            messages.info(request, "Couldn't find that user!")
            return render(request, "auth/approve.html", {"users_list": data})
        
        user.is_active = True
        user.save()

    return render(request, "auth/approve.html", {"users_list": data})

@user_passes_test(is_officer)
def deny_user(request):
    if request.method == "POST":
        n_num = json.loads(request.body)["n_num"]
        user = get_object_or_404(Member, username=n_num)
        if user: user.delete()
        
    return redirect("/auth/approve/")
