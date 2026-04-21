from django.shortcuts import render
from .forms import SearchForm
from .models import Movies


def index(request):
    form = SearchForm()
    results = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            release_date_min = form.cleaned_data['release_date_min']
            release_date_max = form.cleaned_data['release_date_max']
            diameter_min = form.cleaned_data['diameter_min']
            gender = form.cleaned_data['gender']

            results = (
                Movies.objects
                .filter(
                    release_date__gte=release_date_min,
                    release_date__lte=release_date_max,
                    characters__gender=gender,
                    characters__homeworld__diameter__gte=diameter_min,
                )
                .values(
                    'title',
                    'characters__name',
                    'characters__gender',
                    'characters__homeworld__name',
                    'characters__homeworld__diameter',
                )
                .order_by('title', 'characters__name')
            )

    return render(request, 'ex10/index.html', {'form': form, 'results': results})
