import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

from django.views.decorators.csrf import csrf_protect

from .models import Member

# OFFICER DATA. TODO: Replace hardcode, allow superuser to assign officers!
officer_nnumbers = {
    "N501029": "President",
    "N443333": "Vice President",
    "N448323": "Secretary",
    "N463507": "Treasurer",
    "N448061": "Reporter",
    "N441125": "Sergeant At Arms",
}

officer_names = {
    "N501029": "Dominik DiBenedetto",
    "N443333": "Alexander Avin",
    "N448323": "Bella Waleko",
    "N463507": "Jesse Ramsey",
    "N448061": "Christian Leo",
    "N441125": "Nicholas Marmaro",
}

# Helper functions
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

# Views
@csrf_protect
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method != "POST": return render(request, 'auth/login.html')

    username = request.POST.get('username').upper() #nnumber
    password = request.POST.get('password')
    
    if not Member.objects.filter(username=username).exists():
        messages.error(request, 'Invalid N-Number')
        return redirect('/auth/login/')
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        messages.error(request, "Invalid Password")
        return redirect('/auth/login/')
    
    login(request, user)
    update_roles(user) # Check if is matches officer data; TODO: can probably remove once officer assigning is re-worked
    return redirect('/home/')

@csrf_protect
def register_page(request):
    if request.user.is_authenticated: return redirect('/home/')
    if request.method != "POST":  return render(request, 'auth/register.html')

    n_num = request.POST.get('nnumber').upper()
    if not "N" in n_num:  n_num = "N" + n_num

    password = request.POST.get('password')
    conf_password = request.POST.get('confirm-password')
    if password != conf_password:
        messages.info(request, "Passwords don't match!")
        return redirect('/auth/register/')

    user = Member.objects.filter(username=n_num)
    if user.exists():
        messages.info(request, "nNumber already in use!")
        return redirect('/auth/register/')

    name = request.POST.get('name').title()
    email = request.POST.get('email')
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
    update_roles(user)

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