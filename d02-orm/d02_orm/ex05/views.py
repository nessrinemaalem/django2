from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Movies

def populate(request):
    movies = [
        (1, "The Phantom Menace", "Turmoil has engulfed the Galactic Republic. The taxation of trade routes to outlying star systems is in dispute.", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "There is unrest in the Galactic Senate. Several thousand solar systems have declared their intentions to leave the Republic.", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "War! The Republic is crumbling under attacks by the ruthless Sith Lord, Count Dooku.", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (5, "The Empire Strikes Back", "It is a dark time for the Rebellion. Although the Death Star has been destroyed, Imperial troops have driven the Rebel forces from their hidden base and pursued them across the galaxy.", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
        (6, "Return of the Jedi", "Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt.", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25")
    ]

    results = []
    for movie in movies:
        try:
            Movies.objects.create(
                episode_nb=movie[0],
                title=movie[1],
                opening_crawl=movie[2],
                director=movie[3],
                producer=movie[4],
                release_date=movie[5]
            )
            results.append(f"OK - {movie[1]}")
        except Exception as e:
            results.append(f"Erreur pour {movie[1]} : {e}")

    return HttpResponse("<br>".join(results))

def display(request):
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")
    return render(request, 'ex03/display.html', {'movies': movies})

def remove(request):
    try:
        if request.method == "POST":
          ids_to_delete = request.POST.getlist('movies')
          if ids_to_delete:
              ids_to_delete = [int(id) for id in ids_to_delete]
              Movies.objects.filter(episode_nb__in=ids_to_delete).delete()
          return redirect('remove')

        movies = Movies.objects.all()
        return render(request, 'ex05/remove.html', {'movies': movies})
    except Exception as e:
        return HttpResponse(f"Erreur : {e}")