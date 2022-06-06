from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=16)


class Appointment(models.Model):
    starting_time = models.DateTimeField(db_index=True, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, blank=True, null=True)