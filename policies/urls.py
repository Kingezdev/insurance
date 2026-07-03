from django.urls import path
from . import views

app_name = 'policies'

urlpatterns = [
    path('browse/', views.browse_plans_view, name='browse_plans'),
    path('apply/<int:policy_id>/', views.apply_policy_view, name='apply_policy'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('application/<int:application_id>/', views.application_detail_view, name='application_detail'),
]
