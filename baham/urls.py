from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
     path('baham/about-us',views.about,name='aboutus'),
      path('baham/Vehicle',views.view_vehicles,name='Vehicle'),
      path('baham/Create',views.create_vehicle,name='Create'),
]