from django.urls import path
from . import views

urlpatterns =[
    # Maps the endpoint '' to the profile_view function in views.py
path('', views.profile_endpoint, name='profile_endpoints'),

]