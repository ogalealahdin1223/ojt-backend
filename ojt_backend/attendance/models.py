from django.db import models
from django.contrib.auth.models import User


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("incomplete", "Incomplete"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    time_in_1 = models.TimeField(null=True, blank=True)
    time_out_1 = models.TimeField(null=True, blank=True)
    time_in_2 = models.TimeField(null=True, blank=True)
    time_out_2 = models.TimeField(null=True, blank=True)

    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="incomplete")

    class Meta:
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user.username} - {self.date}"

