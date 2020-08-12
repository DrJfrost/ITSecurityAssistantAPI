from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Identification(models.Model):
    id = models.CharField(primary_key=True, max_length=20, verbose_name="id") 


class User(AbstractUser):
    first_name = models.CharField("user's first name", max_length=30)
    last_name = models.CharField("user's last name", max_length=150)
    email = models.EmailField("user's email addresss")
    image = models.ImageField(upload_to="userProfile/", verbose_name="image of user")
    phone = PhoneNumberField(verbose_name="phone of user")

    #Foreign Keys
    identification = models.OneToOneField(Identification, on_delete=models.PROTECT, verbose_name="Identification of user")


class Position(models.Model):
    name = models.CharField(max_length=30, verbose_name="Positions of users")


class StaffProfile(models.Model):
    join_date = models.DateTimeField(verbose_name="Date integration of user", auto_now=True)

    #Foreign Keys
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name="Position of user")
    user = models.OneToOneField(User, related_name="staff_profile", on_delete=models.PROTECT, verbose_name="id of user")
