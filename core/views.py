from django.shortcuts import render
from courses.models import Couse, Module, Material

# Create your views here.
def home(request):
    couses = Couse.objects.all()
    modules = Module.objects.all()
    material = Material.objects.all()
    return render(request, "core/index.html", {"courses": couses, "module": modules, "material": material})

def about(request):
    return render(request, 'core/about.html')

def mentors(request):
    return render(request, 'core/Mentors.html')