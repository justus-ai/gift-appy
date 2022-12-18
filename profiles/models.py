from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


# Create your models here.
class UserProfile(models.Model):
    """User Profile Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=20, null=False, blank=False)
    street_address1 = models.CharField(
        max_length=80, null=False, blank=False)
    street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    town_or_city = models.CharField(
        max_length=40, null=False, blank=False)
    county = models.CharField(
        max_length=80, null=True, blank=True)
    postcode = models.CharField(
        max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label='Country', null=False, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, created, instance, **kwargs):
    """
    Create or Update Profile Models on User save
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Item(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    done = models.BooleanField(null=False, blank=False, default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=False, blank=False)
    link = models.CharField(max_length=350, null=False, blank=False)
    description = models.TextField(max_length=350)

    def __str__(self):
        return self.name
