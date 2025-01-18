from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models



class Profile (models.Model):
    role = models.TextField()
    phone_number = models.TextField()
    email = models.EmailField()
    address = models.TextField()
    about_me = models.TextField()
    leetcode_username = models.TextField()


class DCCUser(AbstractUser):
    # Add any additional fields you need here
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


