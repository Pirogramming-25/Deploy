from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField("닉네임", max_length=50, blank=True)
    bio = models.TextField("소개", blank=True)

    def __str__(self):
        return self.nickname or self.username