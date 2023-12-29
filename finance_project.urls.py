# finance_app/urls.py
from django.urls import path
from .views import process_file

urlpatterns = [
    path('process_file/', process_file, name='process_file'),
]
