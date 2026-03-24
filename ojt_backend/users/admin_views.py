from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance
from .serializers import (
    AdminUserSerializer,
    AdminInternCreateSerializer,
    AdminInternUpdateSerializer,
)


def get_user_role(user):
    if hasattr(user, "ojtprofile"):
        return user.ojtprofile.role
    return None


def get_user_department(user):
    if hasattr(user, "ojtprofile"):
        return user.ojtprofile.department
    return None


def is_superuser_admin(user):
    return user.is_superuser


def is_hr(user):
    return get_user_role(user) == "hr"


def is_supervisor(user):
    return get_user_role(user) == "supervisor"


def is_guard(user):
    return get_user_role(user) == "guard"


def can_view_dashboard(user):
    return is_superuser_admin(user) or is_hr(user) or is_supervisor(user)


def can_view_interns(user):
    return is_superuser_admin(user) or is_hr(user) or is_supervisor(user)


def can_edit_interns(user):
    return is_superuser_admin(user) or is_hr(user)


def filter_interns_by_role(user, interns_queryset):
    if is_superuser_admin(user) or is_hr(user):
        return interns_queryset

    if is_supervisor(user):
        department = get_user_department(user)
        if department:
            return interns_queryset.filter(ojtprofile__department=department)
        return interns_queryset.none()

    return interns_queryset.none()


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_dashboard_summary(request):
    try:
        if not can_view_dashboard(request.user):
            return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

        today = timezone.localdate()

        interns = User.objects.filter(
            is_superuser=False,
            ojtprofile__role="intern"
        ).select_related("ojtprofile")

        interns = filter_interns_by_role(request.user, interns)

        total_interns = interns.count()
        active_interns = interns.filter(is_active=True).count()
        total_attendance_records = Attendance.objects.filter(user__in=interns).count()

        completed_interns = 0
        for intern in interns:
            profile = getattr(intern, "ojtprofile", None)
            required_hours = float(profile.required_hours) if profile and profile.required_hours else 0.0

            completed_hours = Attendance.objects.filter(user=intern).aggregate(
                total=Sum("total_hours")
            )["total"] or 0

            if required_hours > 0 and float(completed_hours) >= required_hours:
                completed_interns += 1

        today_records = Attendance.objects.filter(user__in=interns, date=today)
        present_today = today_records.filter(status="present").count()
        incomplete_today = today_records.filter(status="incomplete").count()

        absent_today = 0
        if today.weekday() != 6:
            absent_today = max(total_interns - today_records.count(), 0)

        response_data = {
            "total_interns": total_interns,
            "active_interns": active_interns,
            "completed_interns": completed_interns,
            "total_attendance_records": total_attendance_records,
            "present_today": present_today,
            "incomplete_today": incomplete_today,
            "absent_today": absent_today,
            "viewer_role": get_user_role(request.user),
        }

        if is_supervisor(request.user):
            response_data["department"] = get_user_department(request.user)

        return Response(response_data)

    except Exception as e:
        return Response(
            {
                "detail": "Dashboard crashed.",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_intern_list(request):
    if not can_view_interns(request.user):
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    search = request.GET.get("search", "").strip()

    interns = User.objects.filter(
        is_superuser=False,
        ojtprofile__role="intern"
    ).select_related("ojtprofile")

    interns = filter_interns_by_role(request.user, interns)

    if search:
        interns = interns.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(ojtprofile__full_name__icontains=search) |
            Q(ojtprofile__trainee_id__icontains=search) |
            Q(ojtprofile__program__icontains=search) |
            Q(ojtprofile__institution__icontains=search) |
            Q(ojtprofile__department__icontains=search) |
            Q(ojtprofile__supervisor__icontains=search)
        )

    data = []
    for intern in interns.order_by("username"):
        profile = getattr(intern, "ojtprofile", None)

        full_name = profile.full_name if profile and profile.full_name else intern.username
        required_hours = float(profile.required_hours) if profile and profile.required_hours else 0.0

        completed_hours = Attendance.objects.filter(user=intern).aggregate(
            total=Sum("total_hours")
        )["total"] or 0

        completed_hours = float(completed_hours)
        remaining_hours = max(required_hours - completed_hours, 0)
        progress = (completed_hours / required_hours * 100) if required_hours > 0 else 0

        data.append({
            "id": intern.id,
            "username": intern.username,
            "email": intern.email,
            "is_active": intern.is_active,
            "full_name": full_name,
            "trainee_id": profile.trainee_id if profile else "",
            "program": profile.program if profile else "",
            "institution": profile.institution if profile else "",
            "department": profile.department if profile else "",
            "supervisor": profile.supervisor if profile else "",
            "required_hours": round(required_hours, 2),
            "completed_hours": round(completed_hours, 2),
            "remaining_hours": round(remaining_hours, 2),
            "progress": round(min(progress, 100), 2),
        })

    return Response({
        "viewer_role": get_user_role(request.user),
        "department": get_user_department(request.user) if is_supervisor(request.user) else None,
        "interns": data,
    })


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_intern_detail(request, user_id):
    if not can_view_interns(request.user):
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    interns = User.objects.filter(
        is_superuser=False,
        ojtprofile__role="intern"
    ).select_related("ojtprofile")

    interns = filter_interns_by_role(request.user, interns)

    try:
        intern = interns.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "Intern not found or not accessible."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminUserSerializer(intern)

    profile = getattr(intern, "ojtprofile", None)
    required_hours = float(profile.required_hours) if profile and profile.required_hours else 0.0

    completed_hours = Attendance.objects.filter(user=intern).aggregate(
        total=Sum("total_hours")
    )["total"] or 0
    completed_hours = float(completed_hours)

    attendance_days = Attendance.objects.filter(
        user=intern,
        status__in=["present", "incomplete"]
    ).count()

    absence_days = 0
    start_date = profile.start_date if profile and profile.start_date else None
    today = timezone.localdate()

    if start_date:
        current = start_date
        while current < today:
            if current.weekday() != 6:
                record_exists = Attendance.objects.filter(user=intern, date=current).exists()
                if not record_exists:
                    absence_days += 1
            current += timedelta(days=1)

    result = serializer.data
    result.update({
        "completed_hours": round(completed_hours, 2),
        "remaining_hours": round(max(required_hours - completed_hours, 0), 2),
        "attendance_days": attendance_days,
        "absence_days": absence_days,
        "viewer_role": get_user_role(request.user),
        "can_edit": can_edit_interns(request.user),
    })

    return Response(result)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_create_intern(request):
    if not can_edit_interns(request.user):
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    serializer = AdminInternCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "Intern account created successfully.",
                "user_id": user.id,
                "username": user.username,
                "role": user.ojtprofile.role,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_update_intern(request, user_id):
    if not can_edit_interns(request.user):
        return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

    try:
        intern = User.objects.select_related("ojtprofile").get(
            id=user_id,
            is_superuser=False,
            ojtprofile__role="intern",
        )
    except User.DoesNotExist:
        return Response({"detail": "Intern not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminInternUpdateSerializer(intern, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Intern updated successfully."})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)