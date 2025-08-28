from django.shortcuts import render
from django.http import HttpResponse
import git
from django.conf import settings
from django.http import JsonResponse

def manifest(request):
    manifest = {
        "name": getattr(settings, "PWA_APP_NAME", ""),
        "short_name": getattr(settings, "PWA_APP_SHORT_NAME", ""),
        "description": getattr(settings, "PWA_APP_DESCRIPTION", ""),
        "start_url": getattr(settings, "PWA_APP_START_URL", "/"),
        "display": getattr(settings, "PWA_APP_DISPLAY", "standalone"),
        "theme_color": getattr(settings, "PWA_APP_THEME_COLOR", "#000000"),
        "background_color": getattr(settings, "PWA_APP_BACKGROUND_COLOR", "#ffffff"),
        "icons": getattr(settings, "PWA_APP_ICONS", []),
        "screenshots": getattr(settings, "PWA_APP_SCREENSHOTS", []),
    }
    return JsonResponse(manifest)


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