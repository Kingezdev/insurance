from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/applications/', views.admin_applications_view, name='admin_applications'),
    path('admin/approve/<int:application_id>/', views.approve_application_view, name='approve_application'),
    path('admin/reject/<int:application_id>/', views.reject_application_view, name='reject_application'),
]
