# coding=utf-8

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import CustomUser


# Create your models here.
class Profile(models.Model):
    """User Profile model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name='Phone #'
    )

    def __str__(self):
        return f'User - {self.user.email}'

    class Meta:
        """Meta class"""
        verbose_name_plural = 'User Profile'


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """create profile"""
    if created:
        Profile.objects.create(user=instance)
