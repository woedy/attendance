"""
URL configuration for PSRS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path

from Attendance import settings
from . import views
from django.conf.urls.static import static
from .views import CustomLogoutView, DeleteStaff, EditStaff, StaffListView, ViewStaff  


urlpatterns = [
    path('', views.custom_login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer_view/<int:customer_id>/', views.customer_view, name='customer_view'),
    path('customer_update/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('customer_delete/<int:customer_id>/', views.customer_delete, name='customer_delete'),
    path('customer_block/<int:customer_id>/', views.customer_block, name='customer_block'),
    path('customer_unblock/<int:customer_id>/', views.customer_unblock, name='customer_unblock'),

    path('logout/', CustomLogoutView.as_view(), name='user-logout'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('profile', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),  
    path('add_staff', views.add_staff, name='add_staff'),
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', ViewStaff.as_view(), name='view_staff'),
    path('staff/<int:pk>/edit/', EditStaff.as_view(), name='edit_staff'),
    path('staff/<int:pk>/delete/', DeleteStaff.as_view(), name='delete_staff'),
    path('process_staff_id/', views.process_staff_id, name='process_staff_id'),
    path('attendance-list/', views.attendance_list, name='attendance_list'),
    path('change_password/', views.change_password, name='change_password'),
    path('download-attendance-csv/', views.download_attendance_csv, name='download_attendance_csv'),
    path('attendance_chart/', views.attendance_chart, name='attendance_chart'),
    path('generate_chart/', views.generate_chart, name='generate_chart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)