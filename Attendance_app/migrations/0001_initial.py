# Generated by Django 5.0.2 on 2024-02-17 13:09

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_letter', models.DateField()),
                ('date_received', models.DateField()),
                ('from_whom_received', models.CharField(max_length=255)),
                ('institutions_reference', models.CharField(max_length=255)),
                ('subject', models.TextField()),
                ('officer_to_whom_file_passed', models.CharField(max_length=255)),
                ('date_filled', models.DateField()),
                ('file_reference_number', models.CharField(max_length=255)),
                ('folio_number', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Messenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_despatched', models.DateField()),
                ('ref_number', models.CharField(max_length=255)),
                ('Messengers_name', models.CharField(max_length=255)),
                ('Name_of_MDA_MMDA', models.CharField(max_length=255)),
                ('Name_of_Receiving_Officer', models.CharField(max_length=255)),
                ('Signature_of_Receiving_Officer', models.CharField(max_length=255)),
                ('date_received', models.DateField()),
                ('Receiving_Officer_Contact_Number', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received_for_despatch', models.DateField()),
                ('date_despatched', models.DateField()),
                ('addressee', models.CharField(max_length=255)),
                ('reference_number', models.CharField(max_length=255)),
                ('folio_number', models.CharField(max_length=255)),
                ('subject', models.TextField()),
                ('mode_of_despatch', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('customer_id', models.CharField(blank=True, max_length=20, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('passport_photo', models.ImageField(upload_to='customer_passports/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customer_groups', to='auth.group', verbose_name='Groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customer_user_permissions', to='auth.permission', verbose_name='User permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
