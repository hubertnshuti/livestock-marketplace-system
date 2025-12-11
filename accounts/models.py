from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extra fields for the built-in User (matches ERD User attributes).
    Keeps User table intact and stores additional attributes here.
    """
    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    registration_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


class Farmer(models.Model):
    """
    Weak entity derived from User. PK is user's id.
    Farmer.UserID (PK & FK -> auth.User)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='farmer_profile')
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.farm_name or self.user.username}"


class Buyer(models.Model):
    """
    Weak entity derived from User. PK is user's id.
    """
    BUYER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('trader', 'Trader'),
        ('butcher', 'Butcher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='buyer_profile')
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE_CHOICES, default='individual')
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.buyer_type})"
