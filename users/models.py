from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value):
    """
    Custom validator function to validate phone numbers.
    """
    if not value.startswith("09") or len(value) != 11 or not value.isdigit():
        raise ValidationError("Phone number must start with 09 and be 11 digits long.")


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    """

    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11, blank=True, null=True, validators=[validate_phone_number]
    )

    def __str__(self):
        return self.email
