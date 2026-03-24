from django.urls import path
from . import admin_views

urlpatterns = [
    path("admin/dashboard/", admin_views.admin_dashboard_summary, name="admin-dashboard"),
    path("admin/interns/", admin_views.admin_intern_list, name="admin-intern-list"),
    path("admin/interns/create/", admin_views.admin_create_intern, name="admin-create-intern"),
    path("admin/interns/<int:user_id>/", admin_views.admin_intern_detail, name="admin-intern-detail"),
    path("admin/interns/<int:user_id>/update/", admin_views.admin_update_intern, name="admin-update-intern"),
]