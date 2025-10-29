from django.db import models
from django.contrib.auth.models import User
from flats.models import Flat

# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='owners')
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    move_in_date = models.DateField(null=True, blank=True)
    is_primary_owner = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.flat.flat_number}"