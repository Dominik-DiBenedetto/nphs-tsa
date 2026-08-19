import json, traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import Event, Team, TeamMember
from .event_recommender import rank_events, get_event_description

from authentication.models import Member

def is_officer(user):
    return user.is_superuser or user.groups.filter(name="Officer").exists()

# Create your views here.
def index(request):
    events_list = Event.objects.all().order_by("name")
    return render(request, "events/index.html", {"Events": events_list})

def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    teams = event.teams.all() or {}

    templated_team_data = []
    for team in teams:
        members = team.competitors.all()
        captain = team.competitors.filter(TeamMember__is_captain=True)
        templated_team_data.append({"team": team, "competitors": members, captain: captain})

    print(templated_team_data, event)
    return render(request, "events/event.html", {"Event": event, "Teams": templated_team_data})

@user_passes_test(is_officer)
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    teams = event.teams.all() or {}

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

            # Proccess teams
            print(teams_json)
            for teamId, members in json.loads(teams_json).items():
                teamNumber = teamId.split("-")[1]
                print(type(teams) is dict)
                team = not type(teams) is dict and teams.filter(number=teamNumber) or None
                if not team:
                    print("New team!")
                    team = Team.objects.create(number=teamNumber)
                for competitor in team.competitors.all():
                    print("COMPETITOR", competitor)
                    if not competitor.name in members:
                        user = Member.objects.get(name=competitor.name)
                        TeamMember.objects.filter(user=user, team=team).delete()
                        print(competitor.name, 'was removed from team!')
                print(teamId)
                for member in members:
                    if member == "None": continue
                    user = Member.objects.get(name=member)
                    if user:
                        TeamMember.objects.create(user=user, team=team, is_captain=False)
                    print(member)

            event.save()
            
            return redirect("/events/", permanent=True)
        except Exception as e:
            print(f"ERRORORO {e}")

    templated_team_data = []
    for team in teams:
        members = team.competitors.all()
        captain = team.competitors.filter(TeamMember__is_captain=True)
        templated_team_data.append({"team": team, "competitors": members, captain: captain})

    print(list(Member.objects.all().values("name")))
    return render(request, "events/update_event.html", {"Event": event, "teams_json": templated_team_data, "members": list(Member.objects.all().values("name"))})

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
