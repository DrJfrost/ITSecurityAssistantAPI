from django.db import models
from users.models import User

# Create your models here.
class MeetingType(models.Model):
    name = models.CharField(max_length=25, verbose_name="Type of meeting")


class MeetingState(models.Model):
    name = models.CharField(max_length=25, verbose_name="State of meeting")


class MeetingClass(models.Model):
    name = models.CharField(max_length=25, verbose_name="State of meeting")


class Meeting(models.Model):
    price = models.FloatField(verbose_name="Price of meeting")
    date = models.DateTimeField(verbose_name="Date of meeting")
    description = models.TextField(verbose_name="Description of meeting")

    #Foreign Keys
    customer = models.ForeignKey(User, related_name="meetings", on_delete=models.PROTECT, verbose_name="Id for user customer")
    auditor = models.ForeignKey(User, related_name="audits", on_delete=models.PROTECT, verbose_name="Id for user auditor")
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.PROTECT, verbose_name="Id for type of meeting")
    state = models.ForeignKey(MeetingState, on_delete=models.PROTECT, default=1, verbose_name="ID for state of meeting")
    meeting_class = models.ForeignKey(MeetingClass, on_delete=models.PROTECT, verbose_name="Id for class of meeting")