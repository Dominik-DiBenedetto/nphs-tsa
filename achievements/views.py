from django.shortcuts import render

# Create your views here.

def achievements_view(request):
    return render(request, "achievements.html")