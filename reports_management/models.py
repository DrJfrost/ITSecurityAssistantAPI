from django.db import models
from users.models import User
from meetings.models import Meeting

# Create your models here.

class OperatingSystem(models.Model):
    name = models.CharField(max_length=25, verbose_name = "The Operating System wich run in a PC")

class SystemType(models.Model):
    name = models.CharField(max_length=25, verbose_name = "Is a type of a system")

class ReportState(models.Model):
    name = models.CharField(max_length=25, verbose_name = "The state of a Report")


class System(models.Model):
    name = models.CharField(max_length=25, verbose_name = "The name from the system")
    description = models.TextField(verbose_name = "Description of the System")

    #Foreign Keys
    OS = models.ForeignKey(OperatingSystem, on_delete=models.PROTECT)
    system_type = models.ForeignKey (SystemType, on_delete=models.PROTECT)
    customer = models.ForeignKey (User, on_delete=models.PROTECT) 

class Complexity(models.Model):
    name = models.CharField(max_length=25, verbose_name="Is the level of complexity that have an user")

class AttackType(models.Model):
    
    name = models.CharField(max_length=30, verbose_name="Is the name of the attack")
    description = models.TextField(verbose_name="Is the description an attack")
    risk = models.PositiveIntegerField(verbose_name="Is the risk level that has an user")

    #Foreign keys
    complexity = models.ForeignKey(Complexity, on_delete=models.PROTECT)

class Report(models.Model):
    
    price = models.FloatField(verbose_name = "The price that you put on a report")
    date = models.DateTimeField(verbose_name = "The date that you did a report")
    diagnostc = models.TextField(verbose_name = "The final diagnostic that an expert does for aproblem")
    solution = models.TextField(verbose_name = "The solution that an expert does for a problem")
    cve_codes = models.TextField(verbose_name = "Is a code for identify a problem in cibersecurity")

    #Foreign Keys 
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT)
    state = models.ForeignKey(ReportState, on_delete=models.PROTECT)
    auditor = models.ForeignKey(User, related_name='reports',on_delete=models.PROTECT)
    analyst = models.ForeignKey(User, related_name='analysis',on_delete=models.PROTECT)
    attacks = models.ForeignKey(AttackType, on_delete=models.PROTECT)