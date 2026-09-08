from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os

def send_view(request):
    return render(request, "send_notification.html")

def firebase_messaging_sw(request):
    sw_path = os.path.join(settings.STATIC_ROOT, "firebase-messaging-sw.js")
    try:
        with open(sw_path, "r") as f:
            content = f.read()
        response = HttpResponse(content, content_type="application/javascript")
        response["Service-Worker-Allowed"] = "/"
        return response
    except FileNotFoundError:
        return HttpResponse("Service worker not found!", status=404)