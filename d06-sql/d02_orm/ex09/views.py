from django.shortcuts import render
from .models import People, Planets


def display(request):
    people = People.objects.filter(
        homeworld__climate__icontains='windy'
    ).order_by('name')
    all_planets = Planets.objects.order_by('name')
    all_people = People.objects.order_by('name')
    return render(request, 'ex09/display.html', {
        'people': people,
        'all_planets': all_planets,
        'all_people': all_people,
    })
