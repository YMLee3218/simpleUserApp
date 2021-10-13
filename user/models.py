from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32)

    class Meta:
        db_table = "Users"
