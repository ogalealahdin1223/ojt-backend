from django.db import models
from django.contrib.auth.models import User


class OJTProfile(models.Model):
    ROLE_CHOICES = [
        ("intern", "Intern"),
        ("supervisor", "Supervisor"),
        ("hr", "HR"),
        ("guard", "Guard"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="intern")

    full_name = models.CharField(max_length=100, blank=True)
    required_hours = models.DecimalField(max_digits=6, decimal_places=2, default=486)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    trainee_id = models.CharField(max_length=100, blank=True)
    intern_type = models.CharField(max_length=100, blank=True)
    program = models.CharField(max_length=255, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    supervisor = models.CharField(max_length=255, blank=True)

    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def assign_role_from_username(self):
        username = str(self.user.username).strip()

        if username.lower() == "admin":
            return "supervisor"

        if username.isdigit() and len(username) == 5:
            first_digit = username[0]

            if first_digit == "1":
                return "supervisor"
            elif first_digit == "2":
                return "hr"
            elif first_digit == "3":
                return "guard"
            elif first_digit in ["4", "5", "6", "7", "8", "9"]:
                return "intern"

        return "intern"

    def save(self, *args, **kwargs):
        self.role = self.assign_role_from_username()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = OJTProfile.objects.create(user=instance)
        profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "ojtprofile"):
        instance.ojtprofile.save()