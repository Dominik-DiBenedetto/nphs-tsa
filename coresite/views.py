from django.shortcuts import render
from authentication.models import Member

# Create your views here.

def home(request):
    return render(request, "index.html")

def members_view(request):
    members = Member.objects.all()
    return render(request, "members.html", {"members": members})