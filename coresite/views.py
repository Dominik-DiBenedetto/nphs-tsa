from django.shortcuts import render
from django.http import HttpResponse
import git

# Create your views here.

def home(request):
    return render(request, "index.html")

def sponsorships(request):
    return render(request, "sponsorships.html")

def sponsors(request):
    return render(request, "sponsors.html")

def update_server(request):
    if request.method == "POST":
        repo = git.Repo("https://github.com/Dominik-DiBenedetto/nphs-tsa.git")
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Success")