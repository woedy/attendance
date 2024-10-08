

from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'first_name',
            'last_name',
            'username', 
            'password',
            'phone_number',
            'gender',
            'passport_photo',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
