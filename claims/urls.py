from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('submit/', views.submit_claim_view, name='submit_claim'),
    path('my-claims/', views.claim_list_view, name='claim_list'),
    path('claim/<int:claim_id>/', views.claim_detail_view, name='claim_detail'),
]
