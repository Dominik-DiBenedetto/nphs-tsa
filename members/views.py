import time, json
from itertools import groupby
from operator import attrgetter

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import Member
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction

from .models import AttendanceRecord
from authentication.views import is_officer

# Views
@login_required
def members_view(request):
    members = Member.objects.all()
    return render(request, "members.html", {"members": members})

@user_passes_test(is_officer)
def delete_member(request):
    if request.method == "POST":
        n_num = request.POST.get('n_num')
        member = get_object_or_404(Member, username=n_num)
        if member: member.delete()

    return redirect("/members/")

@user_passes_test(is_officer)
def update_user(request):
    if request.method != "POST": return

    viewing_nnum = request.POST.get('viewing_nnum')
    viewing_user = get_object_or_404(Member, username=viewing_nnum)
    if not viewing_user: return redirect(f"/members/")

    n_num = request.POST.get('n_num')
    name = request.POST.get('name')
    password = request.POST.get('password')

    viewing_user.username = n_num
    viewing_user.name = name
    
    if password and password != "":
        viewing_user.set_password(password)

    viewing_user.save()
    return redirect(f"/members/{n_num}")

def view_member(request, n_num):
    member = get_object_or_404(Member, username=n_num)
    if not member: return redirect("/members/")

    participating_events = []
    participating_teams = member.teams.all()
    for team in participating_teams:
        event = team.event.first()
        participating_events.append({"id": event.pk, "name": event.name, "team": f"Team {team.number}"})

    return render(request, "view_member.html", {"member": member, "events": participating_events})

def attendance_view(request):
    null_user_records = AttendanceRecord.objects.filter(user__isnull=True)

    for record in null_user_records:
        user = Member.objects.filter(username=record.n_number).first()
        if not user: continue

        record.user = user
        record.save()

    records = AttendanceRecord.objects.select_related('user').order_by('date')
    records_grouped_by_date = {
        date: list(group)
        for date, group in groupby(records, key=attrgetter('date'))
    }

    return render(request, "attendance.html", {"records": records_grouped_by_date})

def scan_attendance_record(request):
    return render(request, "scan_attendance.html", {})

def add_attendance_record(request):
    cached_date = ""
    if request.method == "POST":
        n_num, date = None, None
        if request.META.get("HTTP_SEC_FETCH_DEST", "") == "document": # form submission
            n_num = request.POST.get('n_num').upper()
            date = request.POST.get('date')
        else:
            data = json.loads(request.body)
            n_num = data.get('n_num').upper()
            date = data.get('date')

        cached_date = date

        if not n_num or not date: return render(request, "add_attendance_record.html")
        if "," in n_num:
            n_nums = [(not "N" in num and "N" + num or num) for num in n_num.split(",")]
            user_objs = Member.objects.filter(username__in=n_nums)
            mapped_list = {user.username: user for user in user_objs}
            records = [AttendanceRecord(date=date, n_number=username, user=mapped_list.get(username)) for username in n_nums]

            with transaction.atomic():
                AttendanceRecord.objects.bulk_create(records)
        else:
            if not "N" in n_num: n_num = "N" + n_num

            user_obj = Member.objects.filter(username=n_num).first() or None
            AttendanceRecord.objects.create(
                date = date,
                n_number = n_num,
                user = user_obj
            )

    return render(request, "add_attendance_record.html", {"date": cached_date})
    
def delete_record(request):
    if request.method != "POST": return redirect("/members/attendance/")

    date = request.POST.get("date")
    n_num = request.POST.get("n_num")
    
    record = AttendanceRecord.objects.filter(date=date, n_number=n_num).last()
    if not record: return

    record.delete()
    cache_buster = int(time.time())
    return JsonResponse({
        "redirect_url": f"/members/attendance/?v={cache_buster}"
    })