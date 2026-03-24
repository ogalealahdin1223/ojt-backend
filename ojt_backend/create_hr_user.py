import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ojt_backend.settings")
django.setup()

from django.contrib.auth.models import User

username = "20002"
password = "12345"

user, created = User.objects.get_or_create(username=username)

if created:
    user.set_password(password)
    user.is_staff = False
    user.is_superuser = False
    user.save()
    print(f"User {username} created.")
else:
    user.set_password(password)
    user.save()
    print(f"User {username} already exists. Password updated.")

# Optional: try to ensure OJTProfile exists and role is HR
try:
    from users.models import OJTProfile

    profile, _ = OJTProfile.objects.get_or_create(user=user)
    profile.role = "hr"
    if not profile.full_name:
        profile.full_name = "HR User"
    profile.save()
    print("OJTProfile ensured with role=hr.")
except Exception as e:
    print(f"OJTProfile step skipped or failed: {e}")