from itertools import groupby
from operator import attrgetter
import json
from django.shortcuts import render, redirect
from authentication.models import Member
from .models import AttendanceRecord
from datetime import datetime


# Create your views here.

def members_view(request):
    members = Member.objects.all()
    print(members)
    for member in members:
        print(member.first_name)
        print(member.last_name)
        print(member.name)
    return render(request, "members.html", {"members": members})

def view_member(request, n_num):
    member = Member.objects.get(username=n_num)
    if not member: return redirect("/members/")

    return render(request, "view_member.html", {"member": member})

def attendance_view(request):
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
    print(f"GOT REQUEST {request.method}")
    if request.method == "POST":
        try:
            n_num = request.POST.get('n_num').upper()
            date = request.POST.get('date')
        except:
            body = json.loads(request.body)
            n_num = body["n_num"]
            date = body["date"]

        print(f"N number {n_num} | Date {date}")
        if not n_num or not date:
            return render(request, "add_attendance_record.html")
        
        try:
            user_obj = Member.objects.get(username=n_num)
        except Member.DoesNotExist:
            user_obj = None

        print(user_obj)

        AttendanceRecord.objects.create(
            date = date,
            n_number = n_num,
            user = user_obj
        )

    return render(request, "add_attendance_record.html")
    
def delete_record(request, date, n_num):
    if request.method != "POST": return

    print(n_num)
    date_object = datetime.strptime(date, "%b. %d, %Y")

    # Convert the datetime object to the desired YYYY-MM-DD string format
    date_string = date_object.strftime("%Y-%m-%d")
    print(date_string)
    
    record = AttendanceRecord.objects.get(date=date_string, n_number=n_num)
    print(record)

    if record:
        record.delete()
        return redirect("attendance")