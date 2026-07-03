from django.urls import path
from . import views

app_name = 'premium'

urlpatterns = [
    path('history/', views.premium_history_view, name='premium_history'),
    path('premium/<int:premium_id>/', views.premium_detail_view, name='premium_detail'),
]
