from datetime import datetime, date, timedelta
import calendar
import math

from django.db.models import Sum, Q
from django.utils import timezone

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Attendance
from users.models import OJTProfile


DEFAULT_WORK_HOURS_PER_DAY = 8.0
DEFAULT_DAY_OFF_WEEKDAY = 6  # Sunday (Monday=0 ... Sunday=6)


def get_future_working_days(start_date, days_needed, day_off_weekday=DEFAULT_DAY_OFF_WEEKDAY):
    current_date = start_date
    added_days = 0

    while added_days < days_needed:
        current_date += timedelta(days=1)

        if current_date.weekday() == day_off_weekday:
            continue

        added_days += 1

    return current_date


def calculate_projected_end_date(user, profile):
    if not profile or not profile.start_date:
        return None

    required_hours = float(profile.required_hours or 0)

    completed_hours = Attendance.objects.filter(
        user=user
    ).aggregate(total=Sum("total_hours"))["total"] or 0
    completed_hours = float(completed_hours)

    if completed_hours >= required_hours:
        latest_completed = Attendance.objects.filter(
            user=user
        ).order_by("-date").first()
        return latest_completed.date if latest_completed else timezone.localdate()

    remaining_hours = max(required_hours - completed_hours, 0)

    projected_hours_per_day = DEFAULT_WORK_HOURS_PER_DAY
    if projected_hours_per_day <= 0:
        projected_hours_per_day = 8.0

    days_needed = math.ceil(remaining_hours / projected_hours_per_day)
    today = timezone.localdate()

    projected_date = get_future_working_days(
        start_date=today,
        days_needed=days_needed,
        day_off_weekday=DEFAULT_DAY_OFF_WEEKDAY,
    )

    return projected_date


def calculate_total_hours(attendance, target_date):
    total_seconds = 0

    # First session
    if attendance.time_in_1 and attendance.time_out_1:
        start_1 = datetime.combine(target_date, attendance.time_in_1)
        end_1 = datetime.combine(target_date, attendance.time_out_1)
        diff_1 = (end_1 - start_1).total_seconds()
        if diff_1 > 0:
            total_seconds += diff_1

    # Second session
    if attendance.time_in_2 and attendance.time_out_2:
        start_2 = datetime.combine(target_date, attendance.time_in_2)
        end_2 = datetime.combine(target_date, attendance.time_out_2)
        diff_2 = (end_2 - start_2).total_seconds()
        if diff_2 > 0:
            total_seconds += diff_2

    # No-break direct path: IN1 -> OUT2 only
    elif (
        attendance.time_in_1
        and attendance.time_out_2
        and not attendance.time_out_1
        and not attendance.time_in_2
    ):
        start_direct = datetime.combine(target_date, attendance.time_in_1)
        end_direct = datetime.combine(target_date, attendance.time_out_2)
        diff_direct = (end_direct - start_direct).total_seconds()
        if diff_direct > 0:
            total_seconds = diff_direct

    return round(total_seconds / 3600, 2)


def get_status_from_attendance(attendance, target_date):
    total_hours = calculate_total_hours(attendance, target_date)

    # No break path
    if (
        attendance.time_in_1
        and attendance.time_out_2
        and not attendance.time_out_1
        and not attendance.time_in_2
    ):
        return ("present", total_hours) if total_hours >= 8 else ("incomplete", total_hours)

    # Full with-break path
    if attendance.time_in_1 and attendance.time_out_1 and attendance.time_in_2 and attendance.time_out_2:
        return ("present", total_hours) if total_hours >= 8 else ("incomplete", total_hours)

    return "incomplete", total_hours


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def scan_attendance(request):
    action = request.data.get("action")

    if action not in ["time_in", "time_out"]:
        return Response({
            "success": False,
            "message": "Invalid action."
        }, status=400)

    now = timezone.localtime()
    today = now.date()
    current_time = now.time().replace(microsecond=0)

    attendance, created = Attendance.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={
            "total_hours": 0,
            "status": "incomplete",
        }
    )

    if action == "time_in":
        if attendance.time_in_1 is None:
            attendance.time_in_1 = current_time
            attendance.status = "incomplete"
            attendance.save()

            return Response({
                "success": True,
                "message": "Time In 1 recorded.",
                "type": "time_in_1",
                "date": str(today),
                "time": str(current_time),
            })

        if attendance.time_out_1 is not None and attendance.time_in_2 is None:
            attendance.time_in_2 = current_time
            attendance.status = "incomplete"
            attendance.save()

            return Response({
                "success": True,
                "message": "Time In 2 recorded.",
                "type": "time_in_2",
                "date": str(today),
                "time": str(current_time),
            })

        return Response({
            "success": False,
            "message": "Time In already recorded.",
        }, status=400)

    if action == "time_out":
        if attendance.time_in_1 is None:
            return Response({
                "success": False,
                "message": "You must time in first.",
                "type": "no_time_in",
            }, status=400)

        if attendance.time_out_2 is not None:
            return Response({
                "success": False,
                "message": "Attendance already completed.",
            }, status=400)

        # First timeout
        if attendance.time_out_1 is None:
            start = datetime.combine(today, attendance.time_in_1)
            end = datetime.combine(today, current_time)
            total_hours = round((end - start).total_seconds() / 3600, 2)

            # Auto-complete if 8+ hours without break
            if total_hours >= 8:
                attendance.time_out_2 = current_time
                attendance.total_hours = total_hours
                attendance.status = "present"
                attendance.save()

                return Response({
                    "success": True,
                    "message": "Auto completed (8+ hours).",
                    "type": "time_out_2",
                    "date": str(today),
                    "time": str(current_time),
                    "total_hours": total_hours,
                    "status": "present",
                })

            attendance.time_out_1 = current_time
            attendance.total_hours = total_hours
            attendance.status = "incomplete"
            attendance.save()

            return Response({
                "success": True,
                "message": "Time Out 1 recorded.",
                "type": "time_out_1",
                "date": str(today),
                "time": str(current_time),
                "total_hours": total_hours,
                "status": "incomplete",
            })

        # Final timeout
        if attendance.time_in_2 is None:
            return Response({
                "success": False,
                "message": "You must Time In again after break.",
            }, status=400)

        if attendance.time_out_2 is None:
            attendance.time_out_2 = current_time
            status, total_hours = get_status_from_attendance(attendance, today)
            attendance.total_hours = total_hours
            attendance.status = status
            attendance.save()

            return Response({
                "success": True,
                "message": "Time Out 2 recorded.",
                "type": "time_out_2",
                "date": str(today),
                "time": str(current_time),
                "total_hours": total_hours,
                "status": status,
            })

    return Response({
        "success": False,
        "message": "Attendance could not be processed."
    }, status=400)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user
    today = timezone.localdate()

    profile = OJTProfile.objects.filter(user=user).first()

    completed_hours = Attendance.objects.filter(
        user=user
    ).aggregate(total=Sum("total_hours"))["total"] or 0
    completed_hours = float(completed_hours)

    attendance_days = Attendance.objects.filter(
        user=user
    ).filter(
        Q(status="present") | Q(status="incomplete")
    ).count()

    today_attendance = Attendance.objects.filter(
        user=user,
        date=today
    ).first()

    required_hours = float(profile.required_hours) if profile and profile.required_hours else 486.0
    remaining_hours = max(round(required_hours - completed_hours, 2), 0)

    if required_hours > 0:
        progress_percent = min(round((completed_hours / required_hours) * 100, 2), 100)
    else:
        progress_percent = 0

    projected_end_date = calculate_projected_end_date(user, profile)

    absence_days = 0

    if profile and profile.start_date:
        end_date_for_absence = today - timedelta(days=1)

        if projected_end_date and projected_end_date < end_date_for_absence:
            end_date_for_absence = projected_end_date

        existing_records = Attendance.objects.filter(
            user=user,
            date__gte=profile.start_date,
            date__lte=end_date_for_absence
        )

        attendance_map = {record.date: record for record in existing_records}

        current_date = profile.start_date
        while current_date <= end_date_for_absence:
            if current_date.weekday() != DEFAULT_DAY_OFF_WEEKDAY:
                record = attendance_map.get(current_date)
                if record is None:
                    absence_days += 1

            current_date += timedelta(days=1)

    return Response({
        "success": True,
        "user": {
            "name": profile.full_name if profile and profile.full_name else user.username,
            "username": user.username,
        },
        "summary": {
            "required_hours": required_hours,
            "completed_hours": completed_hours,
            "remaining_hours": remaining_hours,
            "attendance_days": attendance_days,
            "absence_days": absence_days,
            "progress_percent": progress_percent,
            "projected_end_date": str(projected_end_date) if projected_end_date else None,
            "start_date": str(profile.start_date) if profile and profile.start_date else None,
        },
        "today": {
            "date": str(today),
            "time_in_1": str(today_attendance.time_in_1) if today_attendance and today_attendance.time_in_1 else None,
            "time_out_1": str(today_attendance.time_out_1) if today_attendance and today_attendance.time_out_1 else None,
            "time_in_2": str(today_attendance.time_in_2) if today_attendance and today_attendance.time_in_2 else None,
            "time_out_2": str(today_attendance.time_out_2) if today_attendance and today_attendance.time_out_2 else None,
            "status": today_attendance.status if today_attendance else None,
            "total_hours": float(today_attendance.total_hours) if today_attendance else 0,
        }
    })


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def calendar_summary(request):
    user = request.user

    month = request.GET.get("month")
    year = request.GET.get("year")
    selected_date_str = request.GET.get("date")

    today = timezone.localdate()

    month = int(month) if month else today.month
    year = int(year) if year else today.year

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    else:
        selected_date = today

    profile = OJTProfile.objects.filter(user=user).first()
    projected_end_date = calculate_projected_end_date(user, profile)

    month_records = Attendance.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    attendance_map = {record.date: record for record in month_records}

    days_in_month = calendar.monthrange(year, month)[1]
    month_days = []

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        weekday = current_date.weekday()

        status = "none"
        record = attendance_map.get(current_date)

        if profile and profile.start_date:
            if current_date < profile.start_date:
                status = "outside_range"
            elif projected_end_date and current_date > projected_end_date:
                status = "outside_range"
            else:
                if record:
                    status = "attended" if record.status == "present" else "incomplete"
                else:
                    if current_date < today:
                        status = "absent"
                    elif current_date == today:
                        status = "today"
                    else:
                        status = "upcoming"
        else:
            if record:
                status = "attended" if record.status == "present" else "incomplete"

        month_days.append({
            "date": str(current_date),
            "day": day,
            "weekday": weekday,
            "status": status,
        })

    selected_record = Attendance.objects.filter(
        user=user,
        date=selected_date
    ).first()

    return Response({
        "success": True,
        "start_date": str(profile.start_date) if profile and profile.start_date else None,
        "projected_end_date": str(projected_end_date) if projected_end_date else None,
        "month": calendar.month_name[month],
        "year": year,
        "selected_date": str(selected_date),
        "days": month_days,
        "selected_day": {
            "date": str(selected_date),
            "time_in_1": str(selected_record.time_in_1) if selected_record and selected_record.time_in_1 else None,
            "time_out_1": str(selected_record.time_out_1) if selected_record and selected_record.time_out_1 else None,
            "time_in_2": str(selected_record.time_in_2) if selected_record and selected_record.time_in_2 else None,
            "time_out_2": str(selected_record.time_out_2) if selected_record and selected_record.time_out_2 else None,
            "total_hours": float(selected_record.total_hours) if selected_record else 0,
            "status": selected_record.status if selected_record else "No record",
        }
    })


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    profile = OJTProfile.objects.filter(user=user).first()

    return Response({
        "success": True,
        "profile": {
            "full_name": profile.full_name if profile and profile.full_name else "",
            "trainee_id": getattr(profile, "trainee_id", "") if profile else "",
            "required_hours": float(profile.required_hours) if profile and profile.required_hours else 486,
            "intern_type": getattr(profile, "intern_type", "") if profile else "",
            "program": getattr(profile, "program", "") if profile else "",
            "institution": getattr(profile, "institution", "") if profile else "",
            "department": getattr(profile, "department", "") if profile else "",
            "supervisor": getattr(profile, "supervisor", "") if profile else "",
            "profile_image": request.build_absolute_uri(profile.profile_image.url)
            if profile and getattr(profile, "profile_image", None)
            else None,
        }
    })


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_profile_image(request):
    profile = OJTProfile.objects.filter(user=request.user).first()

    if not profile:
        return Response({
            "success": False,
            "message": "Profile not found."
        }, status=404)

    image = request.FILES.get("image")

    if not image:
        return Response({
            "success": False,
            "message": "No image uploaded."
        }, status=400)

    profile.profile_image = image
    profile.save()

    return Response({
        "success": True,
        "message": "Profile image uploaded successfully.",
        "image_url": request.build_absolute_uri(profile.profile_image.url)
    })


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    old_password = request.data.get("old_password", "").strip()
    new_password = request.data.get("new_password", "").strip()
    confirm_password = request.data.get("confirm_password", "").strip()

    if not old_password or not new_password or not confirm_password:
        return Response({
            "success": False,
            "message": "All password fields are required."
        }, status=400)

    user = request.user

    if not user.check_password(old_password):
        return Response({
            "success": False,
            "message": "Old password is incorrect."
        }, status=400)

    if len(new_password) < 6:
        return Response({
            "success": False,
            "message": "New password must be at least 6 characters."
        }, status=400)

    if new_password != confirm_password:
        return Response({
            "success": False,
            "message": "New password and confirm password do not match."
        }, status=400)

    if old_password == new_password:
        return Response({
            "success": False,
            "message": "New password must be different from old password."
        }, status=400)

    user.set_password(new_password)
    user.save()

    Token.objects.filter(user=user).delete()

    return Response({
        "success": True,
        "message": "Password changed successfully. Please login again."
    })