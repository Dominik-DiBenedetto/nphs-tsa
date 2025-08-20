from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html")

def sponsorships(request):
    return render(request, "sponsorships.html")
