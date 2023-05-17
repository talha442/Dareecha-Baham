from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Vehicle
from .enum_types import VehicleType
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    template = loader.get_template(template_name='home.html')
    context = {
        'title': 'Home',
        'heading': 'Welcome to Baham',
    }
    return HttpResponse (template.render(context,request=request))
def about(request):
    context = {
        'title': 'About Us',
        'heading': 'Welcome to Baham',
    }
    template = loader.get_template(template_name='about.html')
    return HttpResponse (template.render(context,request=request))
def create_vehicle(request):
    template = loader.get_template(template_name='createVehicle.html')
    context = {
    'title': 'Vehicles',
    'heading': 'Welcome to Baham',
    'vehicle_types': [t for t in VehicleType]
    }
    return HttpResponse (template.render(context,request=request))
    
def view_vehicles(request):
    template = loader.get_template(template_name='Vehicle.html')
    vehicles = Vehicle.objects.all().order_by('vendor')
    context = {
        'title': 'Vehicles',
        'heading': 'Welcome to Baham',
        'vehicles':  vehicles,
    }
    return HttpResponse (template.render(context,request=request))


def create_vehicle(request):
    template = loader.get_template(template_name='createVehicle.html')
    context = {
    'title': 'Create Vehicles',
    'heading': 'Welcome to Baham',
    'vehicle_types': [t for t in VehicleTypes]
    }

    return HttpResponse (template.render(context,request=request))
    

def delete_vehicle(request, id):
    obj = get_object_or_404(Vehicle, pk = id)
    obj.delete(voided_by=request.user)
    return HttpResponseRedirect(reverse(view_vehicles))

def undelete_vehicle(request, id):
    obj = get_object_or_404(Vehicle, pk = id)
    obj.undelete()
    return HttpResponseRedirect(reverse(view_vehicles))

