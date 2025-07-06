from itertools import groupby
from operator import attrgetter

from django.shortcuts import render
from authentication.models import Member
from .models import AttendanceRecord


# Create your views here.

def members_view(request):
    members = Member.objects.all()
    return render(request, "members.html", {"members": members})

def attendance_view(request):
    records = AttendanceRecord.objects.select_related('user').order_by('date')

    # Group by date
    grouped_by_date = {
        date: list(group)
        for date, group in groupby(records, key=attrgetter('date'))
    }
    print(grouped_by_date)
    return render(request, "attendance.html", {"records": grouped_by_date})

def add_attendance_record(request):
    if request.method == "POST":
        n_num = request.POST.get('n_num').upper()
        date = request.POST.get('date')
        if not n_num or not date:
            print("Maybe API req")
            print(request)
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
    