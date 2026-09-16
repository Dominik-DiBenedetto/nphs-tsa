import json, traceback

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test, login_required

from .event_recommender import rank_events, get_event_description
from .models import Event, Team, TeamMember
from authentication.models import Member

# Helpers
def is_officer(user):
    return user.is_superuser or user.groups.filter(name="Officer").exists()

# Views
def index(request):
    events_list = Event.objects.all().order_by("name")
    return render(request, "events/index.html", {"Events": events_list})

def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    teams = event.teams.all() or []

    templated_team_data = []
    for team in teams:
        members = team.competitors.all()
        captain = team.competitors.filter(teammember__is_captain=True).first()
        templated_team_data.append({"team": team, "competitors": members, "captain": captain})
    return render(request, "events/event.html", {"Event": event, "Teams": templated_team_data})

@user_passes_test(is_officer)
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    teams = event.teams.all().order_by("number")

    templated_team_data = []
    for team in teams:
        captain = team.competitors.filter(teammember__is_captain=True).first()
        competitors = list(team.competitors.all().values_list("name", flat=True))
        templated_team_data.append({"teamNumber": team.number, "captain": captain and captain.name or "None", "competitors": competitors})

    if request.method == "GET": return render(request, "events/update_event.html", {"Event": event, "teams_json": templated_team_data, "members": list(Member.objects.all().values("name"))})

    name = request.POST.get('Name')
    desc = request.POST.get('Description')
    prompt = request.POST.get('Prompt')
    ceg_file = request.FILES.get('CEG')
    teams_json = json.loads(request.POST.get('Teams'))

    event.name = name
    event.desc = desc
    event.prompt = prompt
    event.CEG = ceg_file

    # Proccess teams
    for teamId, teamObj in teams_json.items():
        members = teamObj["Members"]
        teamNumber = teamId.split("-")[1]
        team = not type(teams) is dict and event.teams.filter(number=teamNumber).first() or None

        if not team:
            team = Team.objects.create(number=teamNumber)
            event.teams.add(team)

        for competitor in team.competitors.all():
            if competitor.name in members: continue
            user = Member.objects.get(name=competitor.name)
            TeamMember.objects.filter(user=user, team=team).delete()
        
        for member in members:
            if member == "None": continue
            user = Member.objects.get(name=member)

            if not user: continue
            if team.competitors.filter(name=member).exists():
                team.teammember_set.filter(user=user).update(is_captain=member==teamObj["Captain"])
                continue
            TeamMember.objects.create(user=user, team=team, is_captain=member==teamObj["Captain"])

    saved_teams_count = teams and teams.count() or -1
    updated_teams_count = len(teams_json)

    if saved_teams_count <= updated_teams_count: # No deletions; either unchanged or increased number of teams
        event.save()
        return redirect(f"/events/event/{event_id}", permanent=True)

    # Handle team deletions
    teamNums = sorted([int(teamId.split("-")[1]) for teamId in teams_json ])
    
    if updated_teams_count == 0:
        teams.delete()
    elif (saved_teams_count - updated_teams_count == 1 and (teamNums[0] != 1 or teamNums[-1] != saved_teams_count)):
        if teamNums[0] != 1:
            teams[0].delete()

            teams_queryset = event.teams.all().distinct()
            team_list = (list(teams_queryset) or [])
            team_list.sort(key=lambda t: t.number)
            
            for index, team in enumerate(team_list, start=1):
                if team.number == 0: continue
                team.number = index
    
            Team.objects.bulk_update(team_list, fields=["number"])
        else:
            teams[updated_teams_count].delete()
    else:
        deletionIndices = list(map(lambda pair: pair[1] - 1, filter(lambda pair: pair[1] != pair[0] + 1, zip(teamNums, teamNums[1:]))))
        for team in teams:
            if team.number in deletionIndices: team.delete()

        teams_queryset = event.teams.all().distinct()
        team_list = (list(teams_queryset) or [])
        team_list.sort(key=lambda t: t.number)
        
        for index, team in enumerate(team_list, start=1):
            if team.number in deletionIndices: continue
            team.number = index

        Team.objects.bulk_update(team_list, fields=["number"])


    event.save()
    return redirect(f"/events/event/{event_id}", permanent=True)

@xframe_options_exempt
def view_ceg_file(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        file_path = event.CEG.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf') 
    except (Event.DoesNotExist, FileNotFoundError):
        raise Http404("File not found.")

def event_matchmaker(request):
    if request.method == "POST":
        interests = request.POST.get('interests')
        ranked = rank_events(interests)

        sorted_events_list = []
        for name, _ in ranked:
            eventId = Event.objects.filter(name=name).first()
            if eventId: eventId = eventId.pk
            sorted_events_list.append((name, get_event_description(name), eventId or 1))

        return render(request, "events/matchmaker.html", {"Events": tuple(sorted_events_list)})

    return render(request, "events/matchmaker.html")

def add_event(request):
    if not request.user.groups.filter(name="Officer").exists(): return redirect("/events/")
    if request.method == "GET": return render(request, "events/add_event.html")

    name = request.POST.get('Name').strip()
    desc = request.POST.get('Description').strip()
    prompt = request.POST.get('Prompt').strip()
    ceg_file = request.FILES.get('CEG')
    teams_json = request.POST.get('Teams')

    if not name or not desc: # empty string evaluates to false in python
        return render(request, "events/add_event.html")

    Event.objects.create(
        name = name,
        desc = desc,
        prompt = prompt,
        CEG = ceg_file,
        competitors = teams_json
    )
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
