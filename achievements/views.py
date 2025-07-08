from django.shortcuts import render, redirect
from .models import Conference, EventAchievement
import json
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from events.models import Event

# Create your views here.

def get_achievements(request):
    conferences = Conference.objects.all()
    events = []
    seen_years = {}
    for conference in conferences:
        idx = 0
        if seen_years.get(conference.year) == None: 
            seen_years[conference.year] = len(events)
            idx = len(events)
            events.append({"year": conference.year, "conferences": []})

        year = events[idx]

        conf_events = []
        for event in conference.eventachievement_set.all():
            conf_events.append({
                "event": event.event,
                "students": event.competitors,
                "rank": event.placement
            })

        conf = {
            "name": conference.name,
            "location": conference.location,
            "year": conference.year,
            "date": conference.date,
            "placements": conf_events
        }
        year["conferences"].append(conf)
        
    return JsonResponse(events, safe=False)

def achievements_view(request):
    
    return render(request, "achievements.html")

def add_conference(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data == {}:
            print("EMPTY DATA")
            return redirect("/achievements/")

        dateObj = datetime.strptime(data["date"], "%B %d, %Y").date()
        newConference = Conference.objects.create(
            name=data["name"],
            location=data["location"],
            date=dateObj,
            year=data["year"]
        )
    return redirect("/achievements/")
def add_achievement(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data == {}:
            print("EMPTY DATA")
            return redirect("/achievements/")

        try:
            conference = Conference.objects.get(name=data["conference"], year=data["year"])
        except Exception:
            return redirect("/achievements/")

        event = None
        try:
            event = Event.objects.get(name=data["eventName"])
        except Exception:
            pass

        EventAchievement.objects.create(
            event = data["eventName"],
            competitors = data["students"].replace(", ", ",").split(","),
            placement = data["rank"],
            conference = conference,
            eventRef = event or None,
        )

    return redirect("/achievements/")