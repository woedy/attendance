# Generated by Django 4.2.2 on 2024-02-20 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance_app', '0005_staff_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inward',
        ),
        migrations.DeleteModel(
            name='Messenger',
        ),
        migrations.DeleteModel(
            name='Outward',
        ),
    ]
