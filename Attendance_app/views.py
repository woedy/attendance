from django.urls import path
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')
    
from django.contrib.auth.views import LogoutView
class CustomLogoutView(LogoutView):
    next_page = 'attendance'  
    

from django.db.models import Sum   
from django.utils import timezone
from datetime import datetime, timedelta


@login_required(login_url='custom_login')
def dashboard(request):
    current_date = timezone.now().date()
    start_of_day = timezone.datetime.combine(current_date, timezone.datetime.min.time())
    end_of_day = timezone.datetime.combine(current_date, timezone.datetime.max.time())
    start_of_month = current_date.replace(day=1)
    #end_of_month = start_of_month + relativedelta(months=1) - timedelta(days=1)
    start_of_year = current_date.replace(month=1, day=1)
    #end_of_year = start_of_year + relativedelta(years=1) - timedelta(days=1)

    total_employee = Staff.objects.count()
    total_employee_today = Staff.objects.filter(date__range=(start_of_day, end_of_day)).count()
    total_present = AttendanceLog.objects.filter(date__range=(start_of_day, end_of_day)).count()
    total_abesent = total_employee-total_present
   # total_Emp_Month = AttendanceLog.objects.filter(date__range=(start_of_month, end_of_month)).count()
    #total_abesen_Month = total_employee-total_Emp_Month
    #total_Emp_Year = AttendanceLog.objects.filter(date__range=(start_of_year, end_of_year)).count()
  #  total_Ab_Year = total_employee-total_Emp_Year
    context = {
        'total_employee':total_employee,
        'total_present': total_present,
        'total_abesent': total_abesent,
        #'total_Emp_Month': total_Emp_Month,
        #'total_abesen_Month': total_abesen_Month,
        #'total_Emp_Year': total_Emp_Year,
        #'total_Ab_Year': total_Ab_Year,
        'total_employee_today':total_employee_today,
    }

    return render(request, 'index.html',context)
  
@login_required(login_url='custom_login')  
def profile(request):
    return render(request, 'users-profile.html')  
    
    

from django.shortcuts import render, redirect
from .forms import CustomerForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password  # Import make_password
from django.contrib.auth.models import Group
from django.db import transaction
# @user_passes_test(lambda user: user.groups.filter(name__in=['admin']).exists())
@login_required(login_url='custom_login')
@transaction.atomic
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            plain_password = form.cleaned_data['password']

            hashed_password = make_password(plain_password)

            new_customer = form.save(commit=False)  
            new_customer.password = hashed_password  
            new_customer.save()  
          # Assuming customer is an instance of the Customer model
          
            # customer = Customer.objects.get(id=new_customer.id)
            # group = Group.objects.get(id=2)
            # customer.groups.add(group)

            messages.success(request, 'Customer added successfully.')
            return redirect('create_customer')
        
        else:
            messages.error(request, 'There was an error in the form.')
    else:
        form = CustomerForm()

    return render(request, 'customer.html', {'form': form})


from django.shortcuts import render
from .models import Customer  # Import your Customer model
  
# @user_passes_test(lambda user: user.groups.filter(name__in=['admin']).exists())
@login_required(login_url='custom_login')
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})


from django.shortcuts import render, get_object_or_404, redirect

# @user_passes_test(lambda user: user.groups.filter(name__in=['admin']).exists())
@login_required(login_url='custom_login')
def customer_view(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'customer_view.html', {'customer': customer})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
  
# @user_passes_test(lambda user: user.groups.filter(name__in=['admin']).exists())
@login_required(login_url='custom_login')
def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_list')
        else:
            messages.error(request, 'Error updating customer. Please check the form.')
            messages.error(request, form.errors)

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_update.html', {'form': form, 'customer': customer})
  
# @user_passes_test(lambda user: user.groups.filter(name__in=['admin']).exists())
@login_required(login_url='custom_login')
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customer_delete.html', {'customer': customer})

@login_required(login_url='custom_login')
def customer_block(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = False  
    customer.save()
    return redirect('customer_list') 

@login_required(login_url='custom_login')
def customer_unblock(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = True  
    customer.save()
    return redirect('customer_list') 


# views.py
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

def attendance(request):
    return render(request, 'signInOut.html')

def sign_in(request):
    if request.method == 'POST':
        staff_number = request.POST.get('staffNumber')
        # Perform actions for sign in, such as marking the staff as signed in, 
        # logging the sign-in time, or creating a new attendance record in the database
        return HttpResponse(f'Signed in staff with number: {staff_number}')
    else:
        return HttpResponse('Method not allowed')

def sign_out(request):
    if request.method == 'POST':
        staff_number = request.POST.get('staffNumber')
        # Perform actions for sign out, such as marking the staff as signed out, 
        # logging the sign-out time, or updating the attendance record in the database
        return HttpResponse(f'Signed out staff with number: {staff_number}')
    else:
        return HttpResponse('Method not allowed')


from django.shortcuts import render, redirect
from .forms import StaffForm
@login_required(login_url='custom_login')

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff/") 
        else:
            print("Error", form.errors)
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})


from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Staff
from django.urls import reverse_lazy

class StaffListView(ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'staff_list'

class ViewStaff(DetailView):
    model = Staff
    template_name = 'view_staff.html'
    context_object_name = 'staff'

class EditStaff(UpdateView):
    model = Staff
    fields = ['staff_number', 'first_name', 'last_name', 'middle_name', 'sex', 'current_grade', 'senior_junior', 'Directorate', 'staff_national', 'phone_number']
    template_name = 'edit_staff.html'
    success_url = reverse_lazy('staff_list')
 

class DeleteStaff(DeleteView):
    model = Staff
    template_name = 'delete_staff.html'
    success_url = reverse_lazy('staff_list')
# return JsonResponse({'success': True, 'name': staff.first_name +" "+ staff.last_name+ " Staff ID: "+ staff.staff_number})


from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Staff, AttendanceLog

def process_staff_id(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        action = request.POST.get('action')  # Action: 'sign_in' or 'sign_out'

        if action is None:
            return JsonResponse({'success': False, 'error': 'Action parameter is missing.'})

        if action == 'sign_in':
            return process_sign_in(request, staff_id)
        elif action == 'sign_out':
            return process_sign_out(request, staff_id)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action: {}'.format(action)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

from django.http import JsonResponse
from django.utils import timezone
from .models import Staff, AttendanceLog

def process_sign_in(request, staff_id):
    try:
        staff = Staff.objects.get(staff_number=staff_id)
        today = timezone.now().date()
        existing_log_entry = AttendanceLog.objects.filter(
            Q(staff=staff) & Q(sign_in_time__date=today)
        ).first()

        if existing_log_entry:
            if existing_log_entry.sign_out_time is None:
                return JsonResponse({'success': False, 'error': 'You have already signed in for today.'})
            else:
                return JsonResponse({'success': False, 'error': 'You have already signed out for today.'})
        else:
            new_log_entry = AttendanceLog.objects.create(staff=staff, sign_in_time=timezone.now())
            # Return staff information along with the success message
            return JsonResponse({'success': True, 'staff_number': staff.staff_number, 'first_name': staff.first_name, 'last_name': staff.last_name, 'message': 'You have successfully signed in.'})
    except Staff.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Staff ID not found.'})


def process_sign_out(request, staff_id):
    try:
        staff = Staff.objects.get(staff_number=staff_id)
        today = timezone.now().date()
        existing_log_entry = AttendanceLog.objects.filter(
            Q(staff=staff) & Q(sign_in_time__date=today)
        ).first()

        if existing_log_entry:
            if existing_log_entry.sign_out_time is None:
                existing_log_entry.sign_out_time = timezone.now()
                existing_log_entry.save()
                # Return staff information along with the success message
                return JsonResponse({'success': True, 'staff_number': staff.staff_number, 'first_name': staff.first_name, 'last_name': staff.last_name, 'message': 'You have successfully signed out.'})
            else:
                return JsonResponse({'success': False, 'error': 'You have already signed out for today.'})
        else:
            return JsonResponse({'success': False, 'error': 'You have not signed in for today.'})
    except Staff.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Staff ID not found.'})


from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AttendanceLog
from django.utils import timezone

@login_required(login_url='custom_login')

def attendance_list(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    print(start_date_str)
    print(end_date_str)
    try:
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            attendance_records = AttendanceLog.objects.filter(
                date__gte=start_date,
                date__lte=end_date + timedelta(days=1)  # Include the end date by adding one day
            )

        else:
            # If no date range is selected, show all attendance records
            attendance_records = AttendanceLog.objects.all()

        # Calculate total work time for each attendance record
        for record in attendance_records:
            if record.sign_in_time and record.sign_out_time:
                work_time = record.sign_out_time - record.sign_in_time
                # Format total work time as hours and minutes (HH:MM)
                total_work_time = '{:02d}:{:02d}'.format(
                    work_time.seconds // 3600, (work_time.seconds % 3600) // 60
                )
                record.total_work_time = total_work_time
            else:
                # If sign-in or sign-out time is missing, set total work time as N/A
                record.total_work_time = 'N/A'

            # Add first_name and last_name of the staff member associated with each attendance record
            if record.staff:
                record.first_name = record.staff.first_name
                record.last_name = record.staff.last_name
            else:
                # If no staff member is associated, set first_name and last_name as N/A
                record.first_name = 'N/A'
                record.last_name = 'N/A'

        return render(request, 'attendance_list.html', {'attendance_records': attendance_records})
    except ValueError:
        # Handle invalid date format
        return HttpResponseBadRequest("Invalid date format. Please provide dates in YYYY-MM-DD format.")


# change PWD
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('renewPassword')
        print(current_password)
        print(new_password)
        print(confirm_password)
        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation password do not match.")
            return redirect('change_password')

        # Retrieve the user object
        user = request.user

        # Verify the current password
        hashed_password1 = make_password(current_password)
        print(hashed_password1)
        print(current_password)
        print(user.password)
        if not check_password(hashed_password1, user.password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        # Check if the new password meets any requirements
        # You can add your own password validation logic here
        
        # Hash the new password
        hashed_password = make_password(new_password)

        # Change the user's password
        user.password = hashed_password
        user.save()
        messages.success(request, "Password changed successfully.")
        
        # Redirect to the user profile or login page
        return redirect('user_profile')

    return render(request, 'user-profile.html')


import csv
from django.http import HttpResponse
from .models import AttendanceLog

def download_attendance_csv(request):
    # Retrieve attendance records from the database
    attendance_records = AttendanceLog.objects.all()

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Staff ID', 'Full Name', 'Date', 'Sign In Time', 'Sign Out Time', 'Total Work Time'])

    # Write attendance records to the CSV file
    for record in attendance_records:
        total_work_time = ''
        if record.sign_in_time and record.sign_out_time:
            work_time = record.sign_out_time - record.sign_in_time
            total_work_time = '{:02d}:{:02d}:{:02d}'.format(
                work_time.seconds // 3600, (work_time.seconds % 3600) // 60, work_time.seconds % 60
            )
        writer.writerow([
            record.staff.staff_number,
            f"{record.staff.first_name} {record.staff.last_name}",
            record.sign_in_time.strftime('%Y-%m-%d'),
            record.sign_in_time.strftime('%H:%M:%S') if record.sign_in_time else '',
            record.sign_out_time.strftime('%H:%M:%S') if record.sign_out_time else '',
            total_work_time
        ])

    return response


# views.py
from django.db.models import Count

def get_attendance_data(filter_type, group_by):
    end_date = datetime.now().date()
    if filter_type == 'day':
        start_date = end_date
    elif filter_type == 'week':
        start_date = end_date - timedelta(days=end_date.weekday())
    elif filter_type == 'month':
        start_date = end_date.replace(day=1)
    
    # Filter by senior_junior choice
    if group_by == 'senior_junior':
        attendance_data = AttendanceLog.objects.filter(date__date__gte=start_date, date__date__lte=end_date).values('staff__senior_junior').annotate(num_present=Count('id'))
    else:
        attendance_data = AttendanceLog.objects.filter(date__date__gte=start_date, date__date__lte=end_date).values('date__date').annotate(num_present=Count('id'))
    
    return attendance_data

def attendance_chart(request):
    filter_type = request.GET.get('filter', 'day')  # Default filter is by day
    group_by = request.GET.get('group_by', 'date')  # Default group by is date
    try:
        attendance_data = get_attendance_data(filter_type, group_by)
        
        if group_by == 'senior_junior':
            labels = [entry['staff__senior_junior'] for entry in attendance_data]
        else:
            labels = [entry['date__date'] for entry in attendance_data]
        
        counts = [entry['num_present'] for entry in attendance_data]

        data = {
            'labels': labels,
            'counts': counts,
        }

        return JsonResponse(data)
    except Exception as e:
        error_data = {'error': str(e)}
        return JsonResponse(error_data, status=500)


def generate_chart(request):
        return render(request, 'attendance_chart.html')
