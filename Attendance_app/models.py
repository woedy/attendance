from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    customer_id = models.CharField(max_length=20, unique=True, blank=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    passport_photo = models.ImageField(upload_to='customer_passports/')
    date = models.DateTimeField(auto_now_add=True)    
    
    
    
    def save(self, *args, **kwargs):
        if not self.customer_id:
            # Generate the customer ID by querying the highest existing ID and incrementing it by one
            highest_existing_id = Customer.objects.all().order_by('-customer_id').first()
            if highest_existing_id:
                last_id = int(highest_existing_id.customer_id.split('-')[-1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.customer_id = f'EMP-{new_id:06d}'  # Format with leading zeros if needed
        super(Customer, self).save(*args, **kwargs)
    def __str__(self):
        return self.name



from django.db import models

class Staff(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    SENIOR_JUNIOR_CHOICES = [
        ('Senior', 'Senior'),
        ('Junior', 'Junior'),
    ]
    STAFF_NATIONAL = [
        ('Staff', 'Staff'),
        ('National Service', 'National Service'),
    ]
    
    DIRECTORATE =[
    ('POLICY, PLANNING, BUDGETING, MONITORING AND EVALUATION','POLICY, PLANNING, BUDGETING, MONITORING AND EVALUATION') ,
('HUMAN RESOURCE MANAGEMENT AND DEVELOPMENT','HUMAN RESOURCE MANAGEMENT AND DEVELOPMENT'),
('RESEARCH STATISTICS AND INFORMATION MANAGEMENT','RESEARCH STATISTICS AND INFORMATION MANAGEMENT'),
('GENERAL ADMINISTRATION','GENERAL ADMINISTRATION'),
('FINANCE','FINANCE')
    ]

    staff_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES)
    current_grade = models.CharField(max_length=100)
    senior_junior = models.CharField(max_length=10, choices=SENIOR_JUNIOR_CHOICES)
    phone_number = models.CharField(max_length=15)
    Directorate = models.CharField(max_length=100,choices=DIRECTORATE)
    staff_national = models.CharField(max_length=100,choices=STAFF_NATIONAL)

    date = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.staff_number


class AttendanceLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    sign_in_time = models.DateTimeField(null=True, blank=True)
    sign_out_time = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)    
    image_data = models.BinaryField(null=True, blank=True)  
