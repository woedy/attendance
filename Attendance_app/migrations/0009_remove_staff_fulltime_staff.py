# Generated by Django 5.0.2 on 2024-02-21 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance_app', '0008_rename_highest_qualification_staff_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='fulltime_staff',
        ),
    ]
