from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Event

# Create your views here.
def index(request):
    events_list = Event.objects.all()
    return render(request, "events/index.html", {"Events": events_list})

def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, "events/event.html", {"Event": event})