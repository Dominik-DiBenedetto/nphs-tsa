from itertools import groupby
from operator import attrgetter
import json
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import Member
from .models import AttendanceRecord
from datetime import datetime

from events.models import Event
from django.contrib.auth.decorators import user_passes_test, login_required
from authentication.views import is_officer

# Create your views here.

@login_required
def members_view(request):
    members = Member.objects.all()
    return render(request, "members.html", {"members": members})

@user_passes_test(is_officer)
def delete_member(request):
    if request.method == "POST":
        n_num = request.POST.get('n_num')
        member = get_object_or_404(Member, username=n_num)
        if member:
            member.delete()

    return redirect("/members/")

def view_member(request, n_num):
    try:
        member = Member.objects.get(username=n_num)
    except: return redirect("/members/")

    events = Event.objects.all()
    participating_events = []
    for event in events:
        for team in json.loads(event.competitors):
            if member.name in [memberName.title() for memberName in team["members"]]:
                participating_events.append({"id": event.pk, "name": event.name, "team": f"Team {team['id']}"})
                continue

    return render(request, "view_member.html", {"member": member, "events": participating_events})

def attendance_view(request):
    # Update user references for accounts created after attendance scanned
    null_users = AttendanceRecord.objects.filter(user__isnull=True)
    for user in null_users:
        try:
            user_obj = Member.objects.get(username=user.n_number)
            user.user = user_obj
            user.save()
        except Member.DoesNotExist:
            pass
    
    records = AttendanceRecord.objects.select_related('user').order_by('date')

    # Group by date
    grouped_by_date = {
        date: list(group)
        for date, group in groupby(records, key=attrgetter('date'))
    }
    print(grouped_by_date)
    return render(request, "attendance.html", {"records": grouped_by_date})

def scan_attendance_record(request):
    return render(request, "scan_attendance.html", {})

def add_attendance_record(request):
    if request.method == "POST":
        try:
            n_num = request.POST.get('n_num').upper()
            date = request.POST.get('date')
        except:
            body = json.loads(request.body)
            n_num = body["n_num"]
            date = body["date"]

        if not n_num or not date:
            return render(request, "add_attendance_record.html")
        
        try:
            user_obj = Member.objects.get(username=n_num)
        except Member.DoesNotExist:
            user_obj = None

        AttendanceRecord.objects.create(
            date = date,
            n_number = n_num,
            user = user_obj
        )

    return render(request, "add_attendance_record.html")
    
def delete_record(request, date, n_num):
    if request.method != "POST": return

    date_object = datetime.strptime(date, "%b. %d, %Y")

    # Convert the datetime object to the desired YYYY-MM-DD string format
    date_string = date_object.strftime("%Y-%m-%d")
    
    record = AttendanceRecord.objects.filter(date=date_string, n_number=n_num)
    if record.count() > 1:
        record = record.last()

    if record:
        record.delete()
        return redirect("attendance")