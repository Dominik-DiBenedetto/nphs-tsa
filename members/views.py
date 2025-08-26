from itertools import groupby
from operator import attrgetter
import json
from django.shortcuts import render, redirect
from authentication.models import Member
from .models import AttendanceRecord
from datetime import datetime

from events.models import Event


# Create your views here.

def members_view(request):
    members = Member.objects.all()
    return render(request, "members.html", {"members": members})

def view_member(request, n_num):
    member = Member.objects.get(username=n_num)
    if not member: return redirect("/members/")

    events = Event.objects.all()
    participating_events = []
    for event in events:
        for team in json.loads(event.competitors):
            if member.name in team["members"]:
                participating_events.append({"id": event.pk, "name": event.name, "team": f"Team {team['id']}"})
                continue

    return render(request, "view_member.html", {"member": member, "events": participating_events})

def attendance_view(request):
    records = AttendanceRecord.objects.select_related('user').order_by('date')

    # Group by date
    grouped_by_date = {
        date: list(group)
        for date, group in groupby(records, key=attrgetter('date'))
    }
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
    
    record = AttendanceRecord.objects.get(date=date_string, n_number=n_num)

    if record:
        record.delete()
        return redirect("attendance")