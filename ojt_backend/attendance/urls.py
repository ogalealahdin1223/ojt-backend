from django.urls import path
from .views import scan_attendance, dashboard_summary, calendar_summary, profile_view, change_password, upload_profile_image

urlpatterns = [
    path("scan/", scan_attendance, name="scan_attendance"),
    path("dashboard/", dashboard_summary, name="dashboard_summary"),
    path("calendar/", calendar_summary, name="calendar_summary"),
    path("profile/", profile_view, name="profile_view"),
    path("change-password/", change_password, name="change_password"),
     path("upload-profile-image/", upload_profile_image, name="upload_profile_image"),
]