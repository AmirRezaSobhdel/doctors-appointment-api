# Generated by Django 4.0.4 on 2022-06-06 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ThirtyMinTimeSlot',
            new_name='Appointment',
        ),
    ]
