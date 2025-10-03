from django.db import models
from django.conf import settings

class Principal(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="principal_profile"
    )
    campus = models.OneToOneField(
        "campus.Campus",
        on_delete=models.CASCADE,
        related_name="principal"
    )
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Principal of {self.campus.campus_name}"
