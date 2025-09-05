import json, traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import Event
from .event_recommender import rank_events, get_event_description

def is_officer(user):
    return user.is_superuser or user.groups.filter(name="Officer").exists()

# Create your views here.
def index(request):
    events_list = Event.objects.all()
    return render(request, "events/index.html", {"Events": events_list})

def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    competitors = event.competitors
    try:
        competitors = json.loads(competitors)
    except:
        pass
    return render(request, "events/event.html", {"Event": event, "Teams": competitors})

@user_passes_test(is_officer)
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        try:
            name = request.POST.get('Name')
            desc = request.POST.get('Description')
            prompt = request.POST.get('Prompt')
            ceg_file = request.FILES.get('CEG')
            teams_json = request.POST.get('Teams')

            event.name = name
            event.desc = desc
            event.prompt = prompt
            event.CEG = ceg_file
            event.competitors = teams_json

            event.save()
            
            return redirect("/events/", permanent=True)
        except Exception as e:
            print(f"ERRORORO {e}")

    competitors = event.competitors
    try:
        competitors = json.loads(competitors)
    except:
        pass
    return render(request, "events/update_event.html", {"Event": event, "teams_json": competitors})

@xframe_options_exempt
def view_ceg_file(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        file_path = event.CEG.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # Adjust MIME if needed
    except (Event.DoesNotExist, FileNotFoundError):
        raise Http404("File not found.")

def event_matchmaker(request):
    if request.method == "POST":
        interests = request.POST.get('interests')
        ranked = rank_events(interests)

        sorted_events_list = []
        for name, _ in ranked:
            sorted_events_list.append((name, get_event_description(name)))

        return render(request, "events/matchmaker.html", {"Events": tuple(sorted_events_list)})

    return render(request, "events/matchmaker.html")

def add_event(request):
    if request.user.groups.filter(name="Officer").exists():
        if request.method == "POST":
            try:
                name = request.POST.get('Name')
                desc = request.POST.get('Description')
                prompt = request.POST.get('Prompt')
                ceg_file = request.FILES.get('CEG')
                teams_json = request.POST.get('Teams')

                newEvent = Event.objects.create(
                    name = name,
                    desc = desc,
                    prompt = prompt,
                    CEG = ceg_file,
                    competitors = teams_json
                )
                return redirect("/events/")
                
            except Exception as e:
                print(f"ERROR!!! {e}")
                traceback.print_exc()

        return render(request, "events/add_event.html")
    else:
        return redirect("/events/")

@login_required
def calendar(request):
    return render(request, "member_only_templates/calendar.html")

def delete_event(request, event_id):
    if request.method != "POST": return redirect("/events/")

    event = get_object_or_404(Event, pk=event_id)
    if not event: return redirect("/events/")

    event.delete()
    return redirect("/events/")
